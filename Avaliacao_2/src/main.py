"""Ponto de entrada da automação de cadastro - Portal Fake.

Orquestra o fluxo de ponta a ponta descrito no Mini PDD (seção 6 - Fluxo
Resumido do Processo TO-BE):

1. Acessa a caixa de e-mail e identifica novas solicitações;
2. Baixa os documentos anexados;
3. Valida a documentação conforme as regras de negócio (RN01 a RN04);
4. Classifica o cadastro (Aprovado/Pendente) e organiza os arquivos;
5. Se aprovado, registra os dados na Planilha Mestra;
6. Envia e-mail de resposta ao cliente;
7. Registra em log todas as ações realizadas.

Cada solicitação é processada de forma isolada: uma falha em uma
solicitação é registrada em log e não interrompe o processamento das
demais. Já uma falha de conexão com a caixa de e-mail interrompe a
execução por completo, de forma controlada, para nova tentativa na
próxima execução agendada.
"""

from __future__ import annotations

import sys

from modules.browser_session import sessao_webmail
from modules.config import Config
from modules.email_reader import buscar_novas_solicitacoes
from modules.email_sender import enviar_resposta_cliente
from modules.exceptions import (
    AutomacaoError,
    CaixaEmailIndisponivelError,
    EnvioEmailError,
    PlanilhaMestraError,
)
from modules.file_organizer import organizar_arquivos
from modules.logger_setup import configurar_logger
from modules.models import ResultadoValidacao, Solicitacao
from modules.spreadsheet_writer import inicializar_planilha_mestra, registrar_cadastro_aprovado
from modules.validator import validar_solicitacao


def processar_solicitacao(solicitacao: Solicitacao, page, logger) -> None:
    """Executa o fluxo completo (validação -> organização -> planilha -> resposta)
    para uma única solicitação.
    """
    logger.info("Processando solicitação de CPF %s (%s)", solicitacao.cpf_assunto, solicitacao.remetente)

    resultado: ResultadoValidacao = validar_solicitacao(solicitacao, logger)
    organizar_arquivos(solicitacao, resultado.status, logger)

    if resultado.aprovado:
        try:
            registrar_cadastro_aprovado(resultado.dados_cliente, Config.PLANILHA_MESTRA_PATH, logger)
        except PlanilhaMestraError as erro:
            # Erro identificado, mensagem registrada em log e processo interrompido
            # de forma controlada para esta solicitação: ela será reprocessada na
            # próxima execução, sem enviar uma resposta prematura ao cliente.
            logger.error("Erro identificado: %s. Solicitação NÃO concluída e será reprocessada.", erro.mensagem)
            return

    _enviar_resposta_com_retentativa(page, solicitacao, resultado, logger)


def _enviar_resposta_com_retentativa(page, solicitacao: Solicitacao, resultado: ResultadoValidacao, logger) -> None:
    for tentativa in (1, 2):
        try:
            enviar_resposta_cliente(page, solicitacao, resultado, logger)
            return
        except EnvioEmailError as erro:
            logger.error("Erro identificado (tentativa %d/2): %s", tentativa, erro.mensagem)

    logger.critical(
        "Falha no envio do e-mail de resposta para %s após 2 tentativas. "
        "Sinalizado para análise humana.",
        solicitacao.remetente,
    )


def executar_automacao() -> int:
    """Executa a automação e devolve o código de saída do processo."""
    logger = configurar_logger()
    Config.garantir_diretorios()
    inicializar_planilha_mestra(Config.PLANILHA_MESTRA_PATH)

    logger.info("Iniciando execução da automação de cadastro - Portal Fake")

    try:
        with sessao_webmail(logger) as page:
            solicitacoes = buscar_novas_solicitacoes(page, logger)
            logger.info("%d solicitação(ões) válida(s) para processamento", len(solicitacoes))

            for solicitacao in solicitacoes:
                try:
                    processar_solicitacao(solicitacao, page, logger)
                except AutomacaoError as erro:
                    # Erro de negócio previsto: identificado, registrado em log com
                    # mensagem adequada; o processamento segue para a próxima
                    # solicitação de forma controlada.
                    logger.error(
                        "Erro ao processar solicitação de CPF %s: %s",
                        solicitacao.cpf_assunto,
                        erro.mensagem,
                    )
                except Exception as erro:  # pragma: no cover - rede de segurança
                    # Erro não previsto durante a execução da automação: também é
                    # identificado, registrado em log e não interrompe as demais
                    # solicitações, garantindo finalização controlada do lote.
                    logger.exception(
                        "Erro inesperado ao processar solicitação de CPF %s: %s",
                        solicitacao.cpf_assunto,
                        erro,
                    )

    except CaixaEmailIndisponivelError as erro:
        logger.critical(
            "Execução interrompida: caixa de e-mail indisponível (%s). "
            "O processamento será retomado na próxima execução agendada.",
            erro.mensagem,
        )
        return 1

    logger.info("Execução da automação finalizada com sucesso")
    return 0


if __name__ == "__main__":
    sys.exit(executar_automacao())
