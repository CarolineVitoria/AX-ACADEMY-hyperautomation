"""Testes de document_parser.py, incluindo os cenários de exceção
"Arquivo não encontrado" e "Arquivo corrompido ou ilegível" previstos no
Mini PDD.
"""

import pytest

from modules.document_parser import extrair_dados_ficha_cadastro, extrair_texto_pdf
from modules.exceptions import AnexoNaoEncontradoError, FalhaProcessamentoDocumentoError


def test_extrair_dados_ficha_cadastro_completa(gerar_pdf):
    caminho = gerar_pdf(
        "Ficha_Cadastro_52998224725.pdf",
        [
            "Nome: Maria da Silva",
            "CPF: 529.982.247-25",
            "Data de Nascimento: 10/05/1990",
            "Endereco: Rua das Flores, 123",
        ],
    )

    dados = extrair_dados_ficha_cadastro(caminho)

    assert dados.nome == "Maria da Silva"
    assert dados.cpf == "529.982.247-25"
    assert dados.data_nascimento == "10/05/1990"
    assert dados.endereco == "Rua das Flores, 123"
    assert dados.campos_ausentes == []


def test_extrair_dados_ficha_cadastro_incompleta_reporta_campos_ausentes(gerar_pdf):
    caminho = gerar_pdf("Ficha_Cadastro_incompleta.pdf", ["Nome: Maria da Silva"])

    dados = extrair_dados_ficha_cadastro(caminho)

    assert dados.nome == "Maria da Silva"
    assert "cpf" in dados.campos_ausentes
    assert "data_nascimento" in dados.campos_ausentes
    assert "endereco" in dados.campos_ausentes


def test_anexo_nao_encontrado_levanta_excecao_especifica(tmp_path):
    caminho_inexistente = tmp_path / "Ficha_Cadastro_inexistente.pdf"

    with pytest.raises(AnexoNaoEncontradoError):
        extrair_texto_pdf(caminho_inexistente)


def test_arquivo_corrompido_levanta_excecao_de_falha_no_processamento(tmp_path):
    caminho_corrompido = tmp_path / "Ficha_Cadastro_corrompida.pdf"
    caminho_corrompido.write_bytes(b"isto nao e um arquivo PDF valido")

    with pytest.raises(FalhaProcessamentoDocumentoError):
        extrair_texto_pdf(caminho_corrompido)
