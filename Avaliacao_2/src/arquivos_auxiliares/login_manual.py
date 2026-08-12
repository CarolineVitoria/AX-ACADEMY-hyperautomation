"""Utilitário auxiliar (não faz parte do fluxo automatizado) para autenticar
manualmente na caixa de e-mail UMA VEZ e salvar a sessão (cookies) em disco.

A automação (main.py) reaproveita essa sessão salva em vez de preencher e
submeter o formulário de login programaticamente, evitando o bloqueio
"Este navegador ou app pode não ser seguro" que o Google (e, em menor grau,
a Microsoft) aplica a logins conduzidos por automação de navegador.

Uso:
    python src/arquivos_auxiliares/login_manual.py

Uma janela do navegador será aberta. Faça login normalmente com a conta
configurada em EMAIL_PROVEDOR (.env), incluindo qualquer verificação de
segurança/2FA solicitada. Assim que a caixa de entrada carregar, a sessão é
salva automaticamente e o navegador se fecha sozinho.

A sessão salva expira/pode ser revogada pelo provedor; rode este script
novamente sempre que a automação sinalizar que a caixa de e-mail está
indisponível.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from playwright.sync_api import sync_playwright  # noqa: E402

from modules.browser_session import SELETOR_CAIXA_ENTRADA_CARREGADA, URL_CAIXA_ENTRADA  # noqa: E402
from modules.config import Config  # noqa: E402

TIMEOUT_LOGIN_MANUAL_MS = 5 * 60 * 1000  # até 5 minutos para o login manual


def main() -> None:
    provedor = Config.EMAIL_PROVEDOR
    url = URL_CAIXA_ENTRADA.get(provedor)
    seletor_logado = SELETOR_CAIXA_ENTRADA_CARREGADA.get(provedor)

    if not url:
        print(f"Provedor de e-mail não suportado: '{provedor}' (verifique EMAIL_PROVEDOR no .env)")
        sys.exit(1)

    Config.AUTH_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        navegador = playwright.chromium.launch(
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
        )
        contexto = navegador.new_context()
        pagina = contexto.new_page()
        pagina.goto(url, timeout=30000)

        print("\n>>> Faça login manualmente na janela do navegador que abriu.")
        print(">>> Se houver verificação de segurança/2FA, resolva normalmente.")
        print(">>> Assim que a caixa de entrada carregar, a sessão será salva automaticamente...\n")

        pagina.wait_for_selector(seletor_logado, timeout=TIMEOUT_LOGIN_MANUAL_MS)

        contexto.storage_state(path=str(Config.AUTH_STATE_PATH))
        print(f"Sessão salva em: {Config.AUTH_STATE_PATH}")

        navegador.close()


if __name__ == "__main__":
    main()
