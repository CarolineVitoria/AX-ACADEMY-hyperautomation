"""Leitura da caixa de e-mail e download dos anexos das solicitações de
cadastro (Gmail, via Playwright).

RN01: apenas e-mails com assunto no padrão "Cadastro Portal Fake - CPF do
cliente" são considerados solicitações válidas; os demais são ignorados no
fluxo automático e sinalizados para análise humana (cenário de exceção
"Assunto do e-mail fora do padrão esperado").
"""

from __future__ import annotations

import logging
import re
import urllib.parse
from pathlib import Path

from playwright.sync_api import Locator, Page

from .config import Config
from .cpf_validator import limpar_cpf
from .models import Solicitacao

# Sem âncoras (^/$) e usado com re.search: a filtragem por assunto já é
# feita pela própria busca do Gmail (ver _QUERY_BUSCA), então aqui só
# precisamos localizar o CPF em qualquer lugar do texto da linha.
_PADRAO_ASSUNTO = re.compile(r"Cadastro Portal Fake\s*-\s*(?P<cpf>[\d.\-]+)", re.IGNORECASE)

_QUERY_BUSCA = 'is:unread subject:"Cadastro Portal Fake"'

_MAPA_ANEXO_POR_PREFIXO = {
    "Ficha_Cadastro": "ficha_cadastro",
    "Documento_Foto": "documento_identificacao",
    "Comprovante_Residencia": "comprovante_residencia",
}


def buscar_novas_solicitacoes(page: Page, logger: logging.Logger | None = None) -> list[Solicitacao]:
    """Localiza e-mails não lidos com o assunto no padrão esperado (RN01) e
    baixa os respectivos anexos para uma pasta temporária, organizada por CPF.
    """
    logger = logger or logging.getLogger("portal_fake_automacao")
    solicitacoes: list[Solicitacao] = []

    # Navega direto para a URL de busca do Gmail (em vez de preencher o campo
    # de busca na tela) para não depender do idioma/rótulo da interface. A
    # própria busca já filtra por assunto (subject:), então o robô só
    # precisa lidar com e-mails potencialmente válidos.
    url_busca = "https://mail.google.com/mail/u/0/#search/" + urllib.parse.quote(_QUERY_BUSCA)
    page.goto(url_busca, timeout=30000)
    page.wait_for_load_state("networkidle")

    linhas_email = page.locator("tr.zA")
    total = linhas_email.count()
    logger.info("%d e-mail(s) não lido(s) com assunto 'Cadastro Portal Fake' encontrados", total)

    for indice in range(total):
        linha = linhas_email.nth(indice)
        texto_linha = linha.inner_text()

        correspondencia = _PADRAO_ASSUNTO.search(texto_linha)
        if not correspondencia:
            logger.warning(
                "E-mail não lido ignorado (sinalizado para análise humana): CPF não encontrado "
                "no texto da linha: '%s'",
                texto_linha.replace("\n", " | "),
            )
            continue

        cpf_assunto = limpar_cpf(correspondencia.group("cpf"))
        assunto = f"Cadastro Portal Fake - {cpf_assunto}"
        remetente = _extrair_remetente(linha, logger)

        linha.click()
        page.wait_for_load_state("networkidle")

        pasta_destino = Config.DOWNLOADS_TEMP_DIR / cpf_assunto
        pasta_destino.mkdir(parents=True, exist_ok=True)

        caminhos_anexos = _baixar_anexos(page, pasta_destino, logger)

        solicitacoes.append(
            Solicitacao(
                remetente=remetente,
                assunto=assunto,
                cpf_assunto=cpf_assunto,
                id_mensagem=f"{cpf_assunto}-{indice}",
                caminhos_anexos=caminhos_anexos,
            )
        )

        page.go_back()
        page.wait_for_load_state("networkidle")

    return solicitacoes


def _extrair_remetente(linha: Locator, logger: logging.Logger) -> str:
    """Extrai o e-mail do remetente a partir do atributo `email`, que o
    Gmail expõe internamente nos elementos de remetente (mais estável do
    que depender de uma classe CSS específica, que pode variar).
    """
    elemento = linha.locator("[email]").first
    if elemento.count() > 0:
        endereco = elemento.get_attribute("email")
        if endereco:
            return endereco

    logger.warning("Não foi possível extrair o e-mail do remetente a partir da linha; usando texto bruto")
    return linha.inner_text().strip().splitlines()[0] if linha.inner_text().strip() else ""


def _baixar_anexos(page: Page, pasta_destino: Path, logger: logging.Logger) -> dict[str, Path]:
    caminhos: dict[str, Path] = {}
    # Tenta rótulos em pt-BR e en-US, já que o idioma da interface do Gmail
    # depende da conta e não é controlado pela automação.
    botoes_download = page.locator(
        "span[aria-label^='Baixar'], span[aria-label^='Download'], "
        "a[aria-label^='Baixar'], a[aria-label^='Download']"
    )
    total_botoes = botoes_download.count()

    if total_botoes == 0:
        caminho_print = Config.LOGS_DIR / f"debug_sem_anexos_{pasta_destino.name}.png"
        page.screenshot(path=str(caminho_print))
        logger.warning(
            "Nenhum botão de download de anexo encontrado para o CPF %s "
            "(print salvo em '%s' para depuração do seletor)",
            pasta_destino.name,
            caminho_print,
        )
        return caminhos

    for indice in range(total_botoes):
        with page.expect_download() as info_download:
            botoes_download.nth(indice).click()
        download = info_download.value

        nome_original = download.suggested_filename
        chave = next(
            (
                valor
                for prefixo, valor in _MAPA_ANEXO_POR_PREFIXO.items()
                if nome_original.startswith(prefixo)
            ),
            None,
        )
        if chave is None:
            logger.debug("Anexo '%s' ignorado (fora do padrão de nomenclatura esperado - RN02)", nome_original)
            continue

        caminho_final = pasta_destino / nome_original
        download.save_as(caminho_final)
        caminhos[chave] = caminho_final
        logger.debug("Anexo baixado: '%s'", caminho_final)

    return caminhos
