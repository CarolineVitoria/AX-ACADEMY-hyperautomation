from modules import file_organizer
from modules.models import STATUS_APROVADO, STATUS_PENDENTE, Solicitacao


def _preparar_diretorios(tmp_path, monkeypatch):
    pasta_ok = tmp_path / "Documentos_OK"
    pasta_pendentes = tmp_path / "Documentos_Pendentes"
    monkeypatch.setattr(file_organizer.Config, "DOCUMENTOS_OK_DIR", pasta_ok)
    monkeypatch.setattr(file_organizer.Config, "DOCUMENTOS_PENDENTES_DIR", pasta_pendentes)
    return pasta_ok, pasta_pendentes


def test_organizar_arquivos_move_cadastro_aprovado_para_documentos_ok(tmp_path, monkeypatch):
    pasta_ok, _ = _preparar_diretorios(tmp_path, monkeypatch)

    anexo = tmp_path / "Ficha_Cadastro_52998224725.pdf"
    anexo.write_text("conteudo de teste")

    solicitacao = Solicitacao(
        remetente="cliente@teste.com",
        assunto="Cadastro Portal Fake - 52998224725",
        cpf_assunto="52998224725",
        id_mensagem="msg-1",
        caminhos_anexos={"ficha_cadastro": anexo},
    )

    destino = file_organizer.organizar_arquivos(solicitacao, STATUS_APROVADO)

    assert destino == pasta_ok / "52998224725"
    assert (destino / "Ficha_Cadastro_52998224725.pdf").exists()
    assert not anexo.exists()


def test_organizar_arquivos_move_cadastro_pendente_para_documentos_pendentes(tmp_path, monkeypatch):
    _, pasta_pendentes = _preparar_diretorios(tmp_path, monkeypatch)

    anexo = tmp_path / "Ficha_Cadastro_11144477735.pdf"
    anexo.write_text("conteudo de teste")

    solicitacao = Solicitacao(
        remetente="cliente@teste.com",
        assunto="Cadastro Portal Fake - 11144477735",
        cpf_assunto="11144477735",
        id_mensagem="msg-2",
        caminhos_anexos={"ficha_cadastro": anexo},
    )

    destino = file_organizer.organizar_arquivos(solicitacao, STATUS_PENDENTE)

    assert destino == pasta_pendentes / "11144477735"
    assert (destino / "Ficha_Cadastro_11144477735.pdf").exists()


def test_organizar_arquivos_ignora_anexo_que_nao_existe_mais_em_disco(tmp_path, monkeypatch):
    pasta_ok, _ = _preparar_diretorios(tmp_path, monkeypatch)

    anexo_inexistente = tmp_path / "Ficha_Cadastro_000.pdf"  # nunca criado em disco

    solicitacao = Solicitacao(
        remetente="cliente@teste.com",
        assunto="Cadastro Portal Fake - 000",
        cpf_assunto="000",
        id_mensagem="msg-3",
        caminhos_anexos={"ficha_cadastro": anexo_inexistente},
    )

    destino = file_organizer.organizar_arquivos(solicitacao, STATUS_APROVADO)

    assert destino == pasta_ok / "000"
    assert destino.exists()
