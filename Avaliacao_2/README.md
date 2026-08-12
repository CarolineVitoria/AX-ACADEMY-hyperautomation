# Automação de Cadastro - Portal Fake

Projeto de Hyperautomation desenvolvido para a avaliação da AX Academy Digital Transformation (LG INOVA / Instituto Federal do Amazonas - Campus Manaus Zona Leste / FAEPI).

## 📋 Descrição

A Empresa Portal Fake recebe diariamente, por e-mail, solicitações de cadastro de clientes contendo documentos anexados (ficha de cadastro, documento de identificação e comprovante de residência). Atualmente esse processo é realizado manualmente por um colaborador, que acessa a caixa de entrada, baixa os anexos, confere a documentação, separa os arquivos entre aprovados e pendentes, extrai os dados da ficha de cadastro e preenche uma planilha mestra, respondendo em seguida ao cliente.

Este projeto implementa um robô que automatiza esse fluxo de ponta a ponta, eliminando a execução manual e reduzindo erros humanos.

## 🎯 Objetivo da Automação

Desenvolver uma solução de Hyperautomation capaz de:

- Acessar automaticamente a caixa de e-mail e identificar novas solicitações de cadastro;
- Baixar os documentos anexados a cada solicitação;
- Validar a documentação recebida (nome, CPF, data de nascimento e endereço) conforme as regras de negócio definidas;
- Classificar e organizar os arquivos nas pastas `Documentos_OK/` ou `Documentos_Pendentes/`;
- Extrair os dados da ficha de cadastro e registrá-los na Planilha Mestra;
- Enviar automaticamente uma resposta ao cliente, informando a aprovação do cadastro ou o motivo da pendência.

## 🛠️ Tecnologias Utilizadas

- **Python** — linguagem principal do robô
- **Playwright** — automação de navegador (acesso à caixa de e-mail)
- **openpyxl** — leitura e escrita da Planilha Mestra (.xlsx)
- **pdfplumber / PyPDF2** — extração de dados dos documentos em PDF
- **pytest** — testes automatizados da solução
- **Git & GitHub** — controle de versão, com organização de branches via GitFlow
- **BPMN** — modelagem do processo (AS-IS e TO-BE)

## 📁 Estrutura do Projeto

```
Avaliacao_2/
├── PDD/
│   └── Mini_PDD (2).pdf
├── BPMN/
│   ├── Processo_AS-IS.bpmn      # processo manual (antes da automação)
│   └── Processo_TO-BE.bpmn      # processo automatizado (com tratamento de erro)
├── Projeto_Automacao/
│   ├── Documentos_OK/           # cadastros aprovados (RN05)
│   ├── Documentos_Pendentes/    # cadastros pendentes (RN06)
│   └── Planilha_Mestra.xlsx     # cadastros aprovados (RN07)
├── src/
│   ├── main.py                  # orquestrador do fluxo de ponta a ponta
│   ├── modules/                 # código-fonte organizado por responsabilidade
│   │   ├── browser_session.py   # login na caixa de e-mail via Playwright
│   │   ├── email_reader.py      # identificação e download das solicitações (RN01/RN02)
│   │   ├── email_sender.py      # resposta automática ao cliente (RN08)
│   │   ├── document_parser.py   # extração de dados dos PDFs
│   │   ├── validator.py         # regras de negócio RN01 a RN06
│   │   ├── cpf_validator.py     # validação de CPF (RN03)
│   │   ├── file_organizer.py    # organização em Documentos_OK/Documentos_Pendentes
│   │   ├── spreadsheet_writer.py# leitura/escrita da Planilha Mestra (RN07)
│   │   ├── models.py            # estruturas de dados (Solicitacao, ResultadoValidacao)
│   │   ├── exceptions.py        # exceções customizadas (tratamento de erros)
│   │   ├── config.py            # variáveis de ambiente e caminhos do projeto
│   │   └── logger_setup.py      # configuração do log de execução/auditoria
│   └── arquivos_auxiliares/
│       ├── downloads_temp/                  # pasta temporária de anexos baixados
│       └── gerar_documentos_exemplo.py      # gera PDFs de teste (ver seção 5 abaixo)
├── tests/
│   └── (testes automatizados - pytest)
├── logs/                         # gerado em tempo de execução (execucao_AAAA-MM-DD.log)
├── README.md
├── requirements.txt
├── requirements-dev.txt          # dependências extras para rodar os testes
├── pytest.ini
└── .env.example
```

## ⚙️ Pré-requisitos

- Python 3.10 ou superior
- Git instalado
- Conta de e-mail própria configurada para simular a caixa de entrada da Empresa Portal Fake

## 🚀 Instruções de Execução

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie e ative um ambiente virtual**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   playwright install chromium chrome
   ```
   O canal `chrome` (Google Chrome real, não o Chromium embutido) é necessário para o login manual do próximo passo — veja o motivo abaixo.

   Para rodar os testes automatizados, instale também as dependências de desenvolvimento:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Configure o provedor de e-mail**

   Copie `.env.example` para `.env` na raiz do projeto:
   ```
   EMAIL_PROVEDOR=gmail
   PLAYWRIGHT_HEADLESS=false
   ```
   Não há login/senha no `.env` — a autenticação é manual (próximo passo), justamente para evitar o bloqueio "Este navegador ou app pode não ser seguro" que o Google/Microsoft aplicam a logins conduzidos por automação.

5. **Autentique-se manualmente (uma única vez)**
   ```bash
   python src/arquivos_auxiliares/login_manual.py
   ```
   Uma janela do navegador abre; faça login normalmente com a conta de teste, resolvendo qualquer verificação de segurança/2FA solicitada. Assim que a caixa de entrada carregar, a sessão (cookies) é salva em `src/arquivos_auxiliares/auth_state.json` e o navegador fecha sozinho. A automação (`main.py`) reaproveita essa sessão daqui em diante — sem repetir o login automatizado. Se a caixa de e-mail for sinalizada como indisponível numa execução futura (sessão expirada), rode este script novamente.

   **Por que usamos `channel="chrome"`?** O Chromium embutido do Playwright expõe sinais de automação no próprio navegador (ex.: `navigator.webdriver = true`), que o Google detecta e bloqueia com o aviso "Este navegador ou app pode não ser seguro" — **mesmo em um login 100% manual**. Por isso `login_manual.py` e `browser_session.py` lançam o Google Chrome real (`channel="chrome"`) com a flag `--disable-blink-features=AutomationControlled`, o que resolve o bloqueio na grande maioria dos casos.

   Se o aviso persistir mesmo assim:
   - Acesse [myaccount.google.com/notifications](https://myaccount.google.com/notifications) logo após a tentativa e confirme "Sim, fui eu"; em seguida rode `login_manual.py` novamente — a aprovação libera uma janela curta para completar o login.
   - Ou troque para `EMAIL_PROVEDOR=outlook` no `.env` e use uma conta Outlook/Hotmail de teste, que costuma ser menos agressiva bloqueando automação de navegador.

6. **Envie um e-mail de teste**

   Envie para a caixa configurada um e-mail com o assunto no padrão:
   ```
   Cadastro Portal Fake - CPF do cliente
   ```
   Contendo os anexos:
   - `Ficha_Cadastro_CPF.pdf`
   - `Documento_Foto_CPF.pdf`
   - `Comprovante_Residencia_CPF.pdf`

   Cada PDF deve conter os campos no formato `Campo: valor` (um por linha), por exemplo:
   ```
   Nome: Maria da Silva
   CPF: 529.982.247-25
   Data de Nascimento: 10/05/1990
   Endereco: Rua das Flores, 123 - Manaus/AM
   ```

   Para gerar rapidamente os 3 PDFs de teste já no formato esperado, use o utilitário auxiliar:
   ```bash
   python src/arquivos_auxiliares/gerar_documentos_exemplo.py 52998224725
   ```

7. **Execute o robô**
   ```bash
   python src/main.py
   ```
   O código de saída é `0` em caso de execução concluída (mesmo que solicitações individuais tenham ficado pendentes) e `1` quando a execução foi interrompida por indisponibilidade da caixa de e-mail. O log detalhado de cada execução fica em `logs/execucao_AAAA-MM-DD.log`.

8. **Execute os testes automatizados**
   ```bash
   pytest
   ```

## ⚠️ Tratamento de Exceções

Todas as exceções previstas no Mini PDD (seção 5) são tratadas por classes customizadas em [`src/modules/exceptions.py`](./src/modules/exceptions.py) e cobrem, entre outros, os cenários:

| Cenário | Exceção | Ação |
|---|---|---|
| Arquivo/anexo não encontrado | `AnexoNaoEncontradoError` | Solicitação classificada como PENDENTE; erro registrado em log |
| Dados de entrada inválidos (CPF inválido/divergente, campos ausentes) | `DadosInvalidosError` | Solicitação classificada como PENDENTE; motivo específico informado ao cliente |
| Falha na leitura/processamento de documento (PDF corrompido/ilegível) | `FalhaProcessamentoDocumentoError` | Erro registrado em log; solicitação classificada como PENDENTE |
| Erro durante a gravação na Planilha Mestra | `PlanilhaMestraError` | Erro registrado em log; cadastro não é marcado como concluído e é reprocessado na próxima execução |
| Falha no envio do e-mail de resposta | `EnvioEmailError` | Nova tentativa automática; se persistir, sinalizado para análise humana |
| Caixa de e-mail indisponível/erro de conexão | `CaixaEmailIndisponivelError` | Execução interrompida de forma controlada; reprocessamento na próxima execução agendada |

Em todos os casos o erro é identificado, uma mensagem adequada é registrada no log (console e arquivo) e o processo é finalizado de forma controlada — uma falha em uma solicitação nunca derruba o processamento das demais (ver orquestração em [`src/main.py`](./src/main.py)).

## ✅ Testes Automatizados

A suíte de testes (pytest) cobre as principais funcionalidades da automação: validação de CPF, extração de dados dos PDFs, regras de negócio (RN01–RN06), organização de arquivos, escrita na Planilha Mestra e a orquestração completa do fluxo (incluindo os cenários de exceção acima). Para executar:

```bash
pytest -v
```

## 📄 Documentação Complementar

- [Mini PDD](<./PDD/Mini_PDD (2).pdf>) — descrição detalhada do processo, entradas, saídas, regras de negócio e tratamento de exceções.
- [Diagrama BPMN AS-IS](./BPMN/Processo_AS-IS.bpmn) — processo manual, antes da automação.
- [Diagrama BPMN TO-BE](./BPMN/Processo_TO-BE.bpmn) — processo automatizado pelo robô, com tratamento de erro. Ambos podem ser visualizados em [bpmn.io](https://demo.bpmn.io/) ou no Camunda Modeler.

## 👤 Autor

Projeto desenvolvido individualmente como parte da Avaliação 2 — Turma 102.
