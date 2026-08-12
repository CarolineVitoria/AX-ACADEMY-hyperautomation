"""Testes das regras de negócio RN01 a RN06 (validar_solicitacao)."""

from modules.models import STATUS_APROVADO, STATUS_PENDENTE, Solicitacao
from modules.validator import validar_solicitacao

CPF_VALIDO_1 = "52998224725"
CPF_VALIDO_2 = "11144477735"
CPF_INVALIDO = "11111111111"


def _criar_solicitacao(cpf_assunto: str, caminhos_anexos: dict) -> Solicitacao:
    return Solicitacao(
        remetente="cliente@teste.com",
        assunto=f"Cadastro Portal Fake - {cpf_assunto}",
        cpf_assunto=cpf_assunto,
        id_mensagem="msg-teste",
        caminhos_anexos=caminhos_anexos,
    )


def _criar_documentos_completos(gerar_pdf, cpf: str):
    ficha = gerar_pdf(
        "Ficha_Cadastro.pdf",
        [
            "Nome: Maria da Silva",
            f"CPF: {cpf}",
            "Data de Nascimento: 10/05/1990",
            "Endereco: Rua das Flores, 123",
        ],
    )
    documento = gerar_pdf(
        "Documento_Foto.pdf",
        ["Nome: Maria da Silva", f"CPF: {cpf}", "Data de Nascimento: 10/05/1990"],
    )
    comprovante = gerar_pdf("Comprovante_Residencia.pdf", ["Endereco: Rua das Flores, 123"])
    return {
        "ficha_cadastro": ficha,
        "documento_identificacao": documento,
        "comprovante_residencia": comprovante,
    }


def test_solicitacao_completa_e_aprovada(gerar_pdf):
    anexos = _criar_documentos_completos(gerar_pdf, CPF_VALIDO_1)
    solicitacao = _criar_solicitacao(CPF_VALIDO_1, anexos)

    resultado = validar_solicitacao(solicitacao)

    assert resultado.status == STATUS_APROVADO
    assert resultado.pendencias == []
    assert resultado.dados_cliente["cpf"] == CPF_VALIDO_1
    assert resultado.dados_cliente["nome"] == "Maria da Silva"


def test_solicitacao_sem_nenhum_anexo_fica_pendente():
    solicitacao = _criar_solicitacao(CPF_VALIDO_1, {})

    resultado = validar_solicitacao(solicitacao)

    assert resultado.status == STATUS_PENDENTE
    assert any("Anexo ausente: Ficha de Cadastro" in p for p in resultado.pendencias)
    assert any("Anexo ausente: Documento de Identificação" in p for p in resultado.pendencias)
    assert any("Anexo ausente: Comprovante de Residência" in p for p in resultado.pendencias)


def test_solicitacao_com_cpf_invalido_fica_pendente(gerar_pdf):
    ficha = gerar_pdf(
        "Ficha_Cadastro.pdf",
        [
            "Nome: Maria da Silva",
            f"CPF: {CPF_INVALIDO}",
            "Data de Nascimento: 10/05/1990",
            "Endereco: Rua das Flores, 123",
        ],
    )
    solicitacao = _criar_solicitacao(CPF_INVALIDO, {"ficha_cadastro": ficha})

    resultado = validar_solicitacao(solicitacao)

    assert resultado.status == STATUS_PENDENTE
    assert any("CPF inválido" in p for p in resultado.pendencias)


def test_solicitacao_com_cpf_divergente_entre_documentos_fica_pendente(gerar_pdf):
    ficha = gerar_pdf(
        "Ficha_Cadastro.pdf",
        [
            "Nome: Maria da Silva",
            f"CPF: {CPF_VALIDO_1}",
            "Data de Nascimento: 10/05/1990",
            "Endereco: Rua das Flores, 123",
        ],
    )
    documento = gerar_pdf(
        "Documento_Foto.pdf",
        ["Nome: Maria da Silva", f"CPF: {CPF_VALIDO_2}", "Data de Nascimento: 10/05/1990"],
    )
    comprovante = gerar_pdf("Comprovante_Residencia.pdf", ["Endereco: Rua das Flores, 123"])

    solicitacao = _criar_solicitacao(
        CPF_VALIDO_1,
        {
            "ficha_cadastro": ficha,
            "documento_identificacao": documento,
            "comprovante_residencia": comprovante,
        },
    )

    resultado = validar_solicitacao(solicitacao)

    assert resultado.status == STATUS_PENDENTE
    assert any("divergente" in p for p in resultado.pendencias)


def test_solicitacao_com_campos_incompletos_na_ficha_fica_pendente(gerar_pdf):
    ficha = gerar_pdf("Ficha_Cadastro.pdf", ["Nome: Maria da Silva", f"CPF: {CPF_VALIDO_1}"])
    solicitacao = _criar_solicitacao(CPF_VALIDO_1, {"ficha_cadastro": ficha})

    resultado = validar_solicitacao(solicitacao)

    assert resultado.status == STATUS_PENDENTE
    assert any("data_nascimento" in p for p in resultado.pendencias)
    assert any("endereco" in p for p in resultado.pendencias)
