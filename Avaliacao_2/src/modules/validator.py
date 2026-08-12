"""Validação das solicitações de cadastro conforme as regras de negócio
RN01 a RN06 do Mini PDD.

Este módulo NÃO acessa e-mail nem manipula arquivos/planilhas: recebe uma
Solicitacao já com os anexos baixados em disco e devolve um
ResultadoValidacao (APROVADO ou PENDENTE), sem lançar exceções para
problemas de negócio esperados (anexo ausente, CPF inválido, dados
incompletos) — essas situações são tratadas como PENDÊNCIA, e não como
erro de execução. Erros inesperados de leitura de arquivo continuam sendo
sinalizados via exceções (ver document_parser.py) e tratados pelo chamador.
"""

from __future__ import annotations

import logging

from .cpf_validator import cpf_e_valido, limpar_cpf
from .document_parser import (
    extrair_dados_comprovante_residencia,
    extrair_dados_documento_identificacao,
    extrair_dados_ficha_cadastro,
)
from .exceptions import AnexoNaoEncontradoError, FalhaProcessamentoDocumentoError
from .models import (
    ANEXOS_OBRIGATORIOS,
    STATUS_APROVADO,
    STATUS_PENDENTE,
    ResultadoValidacao,
    Solicitacao,
)

_NOMES_AMIGAVEIS = {
    "ficha_cadastro": "Ficha de Cadastro",
    "documento_identificacao": "Documento de Identificação",
    "comprovante_residencia": "Comprovante de Residência",
}


def validar_solicitacao(
    solicitacao: Solicitacao, logger: logging.Logger | None = None
) -> ResultadoValidacao:
    """Aplica as regras de negócio RN01 a RN06 sobre uma solicitação.

    Retorna um ResultadoValidacao com status APROVADO (todas as
    verificações passaram) ou PENDENTE (com a lista de pendências
    encontradas, usada tanto no log quanto na resposta ao cliente).
    """
    logger = logger or logging.getLogger("portal_fake_automacao")
    pendencias: list[str] = []

    # RN02: os 3 anexos obrigatórios precisam estar presentes.
    for chave, nome_amigavel in _NOMES_AMIGAVEIS.items():
        if chave not in solicitacao.caminhos_anexos:
            pendencias.append(f"Anexo ausente: {nome_amigavel}")

    dados_ficha = dados_documento = dados_comprovante = None

    if "ficha_cadastro" in solicitacao.caminhos_anexos:
        dados_ficha = _extrair_com_tratamento(
            extrair_dados_ficha_cadastro,
            solicitacao.caminhos_anexos["ficha_cadastro"],
            _NOMES_AMIGAVEIS["ficha_cadastro"],
            pendencias,
            logger,
        )

    if "documento_identificacao" in solicitacao.caminhos_anexos:
        dados_documento = _extrair_com_tratamento(
            extrair_dados_documento_identificacao,
            solicitacao.caminhos_anexos["documento_identificacao"],
            _NOMES_AMIGAVEIS["documento_identificacao"],
            pendencias,
            logger,
        )

    if "comprovante_residencia" in solicitacao.caminhos_anexos:
        dados_comprovante = _extrair_com_tratamento(
            extrair_dados_comprovante_residencia,
            solicitacao.caminhos_anexos["comprovante_residencia"],
            _NOMES_AMIGAVEIS["comprovante_residencia"],
            pendencias,
            logger,
        )

    # RN04: nome, CPF, data de nascimento e endereço devem constar de forma
    # legível e completa (avaliado apenas para os documentos que puderam ser lidos).
    if dados_ficha:
        for campo in dados_ficha.campos_ausentes:
            pendencias.append(f"Campo '{campo}' ausente/ilegível na Ficha de Cadastro")
    if dados_documento:
        for campo in dados_documento.campos_ausentes:
            pendencias.append(
                f"Campo '{campo}' ausente/ilegível no Documento de Identificação"
            )
    if dados_comprovante:
        for campo in dados_comprovante.campos_ausentes:
            pendencias.append(
                f"Campo '{campo}' ausente/ilegível no Comprovante de Residência"
            )

    # RN03: CPF válido e coincidente em todos os documentos e no assunto do e-mail.
    cpfs_brutos = {"assunto do e-mail": solicitacao.cpf_assunto}
    if dados_ficha and dados_ficha.cpf:
        cpfs_brutos["Ficha de Cadastro"] = dados_ficha.cpf
    if dados_documento and dados_documento.cpf:
        cpfs_brutos["Documento de Identificação"] = dados_documento.cpf

    cpfs_encontrados = {
        origem: limpar_cpf(cpf) for origem, cpf in cpfs_brutos.items() if cpf
    }

    if cpfs_encontrados:
        cpf_referencia = next(iter(cpfs_encontrados.values()))
        if not cpf_e_valido(cpf_referencia):
            pendencias.append(f"CPF inválido: {cpf_referencia}")
        elif len(set(cpfs_encontrados.values())) > 1:
            pendencias.append(
                "CPF divergente entre o assunto do e-mail e os documentos enviados"
            )

    if pendencias:
        logger.warning(
            "Solicitação %s classificada como PENDENTE: %s",
            solicitacao.cpf_assunto,
            "; ".join(pendencias),
        )
        return ResultadoValidacao(status=STATUS_PENDENTE, pendencias=pendencias)

    dados_cliente = {
        "nome": dados_ficha.nome,
        "cpf": limpar_cpf(dados_ficha.cpf),
        "data_nascimento": dados_ficha.data_nascimento,
        "endereco": dados_ficha.endereco,
    }
    logger.info("Solicitação %s classificada como APROVADO", solicitacao.cpf_assunto)
    return ResultadoValidacao(status=STATUS_APROVADO, dados_cliente=dados_cliente)


def _extrair_com_tratamento(funcao_extracao, caminho, nome_amigavel, pendencias, logger):
    """Executa a extração de um documento tratando falhas de leitura como pendência.

    Cobre os cenários de exceção "Arquivo não encontrado" e "Arquivo
    corrompido ou ilegível": o erro é registrado em log e a solicitação
    segue o fluxo normal, sendo classificada como PENDENTE em vez de
    interromper o processamento das demais solicitações.
    """
    try:
        return funcao_extracao(caminho)
    except AnexoNaoEncontradoError as erro:
        logger.error("Anexo não encontrado ao validar '%s': %s", nome_amigavel, erro.mensagem)
        pendencias.append(f"Anexo não encontrado: {nome_amigavel}")
    except FalhaProcessamentoDocumentoError as erro:
        logger.error(
            "Falha na leitura/processamento de '%s': %s", nome_amigavel, erro.mensagem
        )
        pendencias.append(f"Não foi possível ler o documento: {nome_amigavel}")
    return None
