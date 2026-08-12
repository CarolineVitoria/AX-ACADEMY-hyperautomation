"""Envio da resposta automática ao cliente, via Gmail/Playwright (RN08)."""

from __future__ import annotations

import logging

from playwright.sync_api import Page

from .exceptions import EnvioEmailError
from .models import STATUS_APROVADO, ResultadoValidacao, Solicitacao

_ASSUNTO_RESPOSTA = "Retorno - Cadastro Portal Fake"


def enviar_resposta_cliente(
    page: Page,
    solicitacao: Solicitacao,
    resultado: ResultadoValidacao,
    logger: logging.Logger | None = None,
) -> None:
    """Envia ao cliente a confirmação de aprovação ou o motivo da pendência (RN08).

    Levanta EnvioEmailError em caso de falha, para que o chamador possa
    registrar o erro e tentar reenviar (cenário de exceção "Falha no envio
    do e-mail de resposta ao cliente").
    """
    logger = logger or logging.getLogger("portal_fake_automacao")
    corpo = _montar_corpo(resultado)

    try:
        page.click("div[gh='cm']")  # botão "Escrever"
        page.wait_for_selector("textarea[name='to']", timeout=10000)
        page.fill("textarea[name='to']", solicitacao.remetente)
        page.fill("input[name='subjectbox']", _ASSUNTO_RESPOSTA)
        page.fill("div[aria-label='Corpo da mensagem']", corpo)
        page.click("div[aria-label='Enviar']")
        page.wait_for_timeout(1000)
    except Exception as erro:
        raise EnvioEmailError(
            f"Falha ao enviar e-mail de resposta para {solicitacao.remetente}: {erro}"
        ) from erro

    logger.info(
        "E-mail de resposta enviado para %s (status: %s)", solicitacao.remetente, resultado.status
    )


def _montar_corpo(resultado: ResultadoValidacao) -> str:
    if resultado.status == STATUS_APROVADO:
        return (
            "Olá,\n\nSeu cadastro no Portal Fake foi APROVADO com sucesso.\n\n"
            "Atenciosamente,\nEquipe Portal Fake"
        )
    return (
        "Olá,\n\nSeu cadastro no Portal Fake ficou PENDENTE pelo(s) seguinte(s) motivo(s):\n"
        f"- {resultado.motivo}\n\n"
        "Por favor, reenvie a solicitação com a documentação corrigida.\n\n"
        "Atenciosamente,\nEquipe Portal Fake"
    )
