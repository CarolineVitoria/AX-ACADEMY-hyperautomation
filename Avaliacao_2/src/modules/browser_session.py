"""Sessão de navegador (Playwright) usada para acessar a caixa de e-mail via
interface web, conforme especificado no Mini PDD (Ferramentas: Python +
Playwright).

A autenticação é feita manualmente uma única vez, com
`arquivos_auxiliares/login_manual.py`, que salva a sessão (cookies) em
`Config.AUTH_STATE_PATH`. A automação apenas reaproveita essa sessão salva,
em vez de preencher e submeter o formulário de login programaticamente —
esse tipo de login automatizado é rotineiramente bloqueado pelo Google/
Microsoft com o aviso "Este navegador ou app pode não ser seguro".
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Iterator

from playwright.sync_api import Browser, Page, sync_playwright

from .config import Config
from .exceptions import CaixaEmailIndisponivelError

URL_CAIXA_ENTRADA = {
    "gmail": "https://mail.google.com/",
    "outlook": "https://outlook.live.com/mail/",
}

SELETOR_CAIXA_ENTRADA_CARREGADA = {
    "gmail": "[gh='tl']",
    "outlook": "div[role='main']",
}


@contextmanager
def sessao_webmail(logger: logging.Logger | None = None) -> Iterator[Page]:
    """Abre o navegador reaproveitando a sessão autenticada salva e cede a
    página já logada para o chamador.

    Cobre o cenário de exceção "Erro de conexão/indisponibilidade da caixa
    de e-mail": tanto a ausência de uma sessão salva quanto qualquer falha
    durante a abertura do navegador são convertidas em
    CaixaEmailIndisponivelError, para que o chamador interrompa a execução
    de forma controlada e registre o erro em log.
    """
    logger = logger or logging.getLogger("portal_fake_automacao")
    provedor = Config.EMAIL_PROVEDOR
    url = URL_CAIXA_ENTRADA.get(provedor)
    if url is None:
        raise CaixaEmailIndisponivelError(f"Provedor de e-mail não suportado: '{provedor}'")

    if not Config.AUTH_STATE_PATH.exists():
        raise CaixaEmailIndisponivelError(
            "Nenhuma sessão autenticada encontrada. Execute uma vez: "
            "python src/arquivos_auxiliares/login_manual.py"
        )

    try:
        with sync_playwright() as playwright:
            navegador: Browser = playwright.chromium.launch(
                headless=Config.PLAYWRIGHT_HEADLESS,
                channel="chrome",
                args=["--disable-blink-features=AutomationControlled"],
            )
            contexto = navegador.new_context(
                accept_downloads=True, storage_state=str(Config.AUTH_STATE_PATH)
            )
            pagina = contexto.new_page()
            pagina.goto(url, timeout=30000)
            pagina.wait_for_selector(SELETOR_CAIXA_ENTRADA_CARREGADA[provedor], timeout=30000)
            logger.info("Sessão autenticada reaproveitada com sucesso (%s)", provedor)
            try:
                yield pagina
            finally:
                # Renova o arquivo de sessão com os cookies mais recentes,
                # prolongando sua validade para as próximas execuções.
                contexto.storage_state(path=str(Config.AUTH_STATE_PATH))
                navegador.close()
    except CaixaEmailIndisponivelError:
        raise
    except Exception as erro:
        logger.error("Falha de conexão/indisponibilidade da caixa de e-mail: %s", erro)
        raise CaixaEmailIndisponivelError(
            f"{erro} — a sessão salva pode ter expirado; rode novamente "
            "python src/arquivos_auxiliares/login_manual.py"
        ) from erro
