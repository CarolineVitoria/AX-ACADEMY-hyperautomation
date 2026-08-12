from modules.cpf_validator import cpf_e_valido, formatar_cpf, limpar_cpf


def test_cpf_valido_com_formatacao_e_aceito():
    assert cpf_e_valido("529.982.247-25") is True


def test_cpf_valido_sem_formatacao_e_aceito():
    assert cpf_e_valido("52998224725") is True


def test_cpf_com_digito_verificador_incorreto_e_invalido():
    assert cpf_e_valido("529.982.247-26") is False


def test_cpf_com_todos_digitos_iguais_e_invalido():
    assert cpf_e_valido("111.111.111-11") is False


def test_cpf_com_quantidade_incorreta_de_digitos_e_invalido():
    assert cpf_e_valido("123456") is False


def test_cpf_vazio_e_invalido():
    assert cpf_e_valido("") is False


def test_limpar_cpf_remove_pontuacao():
    assert limpar_cpf("529.982.247-25") == "52998224725"


def test_formatar_cpf_aplica_mascara_padrao():
    assert formatar_cpf("52998224725") == "529.982.247-25"


def test_formatar_cpf_com_tamanho_invalido_retorna_valor_original():
    assert formatar_cpf("123") == "123"
