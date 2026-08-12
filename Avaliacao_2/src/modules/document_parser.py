"""Extração de dados dos documentos PDF (Ficha de Cadastro, Documento de
Identificação e Comprovante de Residência).

Os documentos são lidos como texto (linhas no formato "Campo: valor") e os
campos relevantes (nome, CPF, data de nascimento e endereço) são extraídos
por expressão regular. Cobre a RN04: "O robô deve conferir se nome, CPF,
data de nascimento e endereço constam de forma legível e completa nos
documentos."
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import pdfplumber

from .exceptions import AnexoNaoEncontradoError, FalhaProcessamentoDocumentoError

_PADROES_CAMPOS = {
    "nome": re.compile(r"nome\s*:\s*(.+)", re.IGNORECASE),
    "cpf": re.compile(r"cpf\s*:\s*(.+)", re.IGNORECASE),
    "data_nascimento": re.compile(
        r"data\s*(?:de)?\s*nascimento\s*:\s*(.+)", re.IGNORECASE
    ),
    "endereco": re.compile(r"endere[çc]o\s*:\s*(.+)", re.IGNORECASE),
}


@dataclass
class DadosDocumento:
    """Campos extraídos de um documento, com o registro de quais faltaram."""

    nome: str | None = None
    cpf: str | None = None
    data_nascimento: str | None = None
    endereco: str | None = None
    campos_ausentes: list[str] = field(default_factory=list)

    def esta_completo(self, campos_esperados: list[str]) -> bool:
        return all(getattr(self, campo) for campo in campos_esperados)


def extrair_texto_pdf(caminho_arquivo: Path) -> str:
    """Extrai todo o texto de um PDF.

    Levanta AnexoNaoEncontradoError se o arquivo não existir e
    FalhaProcessamentoDocumentoError se o PDF não puder ser lido
    (arquivo corrompido/ilegível).
    """
    if not caminho_arquivo.exists():
        raise AnexoNaoEncontradoError(caminho_arquivo.name)

    try:
        texto_paginas = []
        with pdfplumber.open(caminho_arquivo) as pdf:
            for pagina in pdf.pages:
                texto_paginas.append(pagina.extract_text() or "")
        texto = "\n".join(texto_paginas)
    except Exception as erro:  # pdfplumber/pypdf podem levantar diferentes exceções
        raise FalhaProcessamentoDocumentoError(caminho_arquivo.name, str(erro)) from erro

    if not texto.strip():
        raise FalhaProcessamentoDocumentoError(
            caminho_arquivo.name, "documento sem texto legível (possível falha de OCR)"
        )

    return texto


def _extrair_campos(texto: str, campos_esperados: list[str]) -> DadosDocumento:
    dados = DadosDocumento()
    for campo in campos_esperados:
        padrao = _PADROES_CAMPOS[campo]
        correspondencia = padrao.search(texto)
        valor = correspondencia.group(1).strip() if correspondencia else ""
        if valor:
            setattr(dados, campo, valor)
        else:
            dados.campos_ausentes.append(campo)
    return dados


def extrair_dados_ficha_cadastro(caminho_arquivo: Path) -> DadosDocumento:
    """Extrai nome, CPF, data de nascimento e endereço da Ficha de Cadastro."""
    texto = extrair_texto_pdf(caminho_arquivo)
    return _extrair_campos(texto, ["nome", "cpf", "data_nascimento", "endereco"])


def extrair_dados_documento_identificacao(caminho_arquivo: Path) -> DadosDocumento:
    """Extrai nome, CPF e data de nascimento do Documento de Identificação."""
    texto = extrair_texto_pdf(caminho_arquivo)
    return _extrair_campos(texto, ["nome", "cpf", "data_nascimento"])


def extrair_dados_comprovante_residencia(caminho_arquivo: Path) -> DadosDocumento:
    """Extrai o endereço do Comprovante de Residência."""
    texto = extrair_texto_pdf(caminho_arquivo)
    return _extrair_campos(texto, ["endereco"])
