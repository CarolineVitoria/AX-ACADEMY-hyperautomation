"""Exceções customizadas da automação de cadastro - Portal Fake.

Cada exceção representa um cenário de erro previsto no Mini PDD (seção 5 -
Tratamento de Exceções) e carrega uma mensagem amigável, adequada para ser
exibida ao usuário/log e, quando aplicável, reaproveitada na resposta
automática enviada ao cliente.
"""

from __future__ import annotations


class AutomacaoError(Exception):
    """Classe base para todos os erros previstos da automação."""

    def __init__(self, mensagem: str) -> None:
        self.mensagem = mensagem
        super().__init__(mensagem)


class CaixaEmailIndisponivelError(AutomacaoError):
    """Erro de conexão/indisponibilidade da caixa de e-mail.

    Ação prevista no PDD: interromper a execução, registrar o erro em log
    e reiniciar o processamento na próxima execução agendada.
    """


class AnexoNaoEncontradoError(AutomacaoError):
    """Um ou mais anexos obrigatórios (RN02) não foram encontrados.

    Cenário de exceção: "Arquivo não encontrado".
    """

    def __init__(self, nome_anexo_faltante: str) -> None:
        self.nome_anexo_faltante = nome_anexo_faltante
        super().__init__(
            f"Anexo obrigatório não encontrado: '{nome_anexo_faltante}'."
        )


class DadosInvalidosError(AutomacaoError):
    """Dados de entrada inválidos ou incompletos (RN03/RN04).

    Cobre CPF inválido/divergente e campos ausentes na Ficha de Cadastro.
    """

    def __init__(self, motivo: str) -> None:
        self.motivo = motivo
        super().__init__(f"Dados de entrada inválidos: {motivo}")


class FalhaProcessamentoDocumentoError(AutomacaoError):
    """Falha na leitura/processamento de um documento (PDF corrompido/ilegível)."""

    def __init__(self, nome_arquivo: str, causa: str) -> None:
        self.nome_arquivo = nome_arquivo
        self.causa = causa
        super().__init__(
            f"Falha ao ler/processar o documento '{nome_arquivo}': {causa}"
        )


class PlanilhaMestraError(AutomacaoError):
    """Erro durante a leitura/gravação da Planilha Mestra."""


class EnvioEmailError(AutomacaoError):
    """Falha no envio do e-mail de resposta ao cliente."""


class ErroExecucaoAutomacaoError(AutomacaoError):
    """Erro genérico e não previsto durante a execução da automação.

    Usado como rede de segurança no orquestrador (main.py) para garantir que
    qualquer falha não mapeada ainda seja tratada de forma controlada.
    """
