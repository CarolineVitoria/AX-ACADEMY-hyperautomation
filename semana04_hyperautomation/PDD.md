# PDD PORTAL FAKE
## Objetivo:
O portal permite o cadastro, consulta e exportação de dados de usuários.

## Escopo:
- Cadastro de usuário
- Valida o dado do usuário
- Permite a busca dos dados do usuário
- Alteração de dados do usuário
- Exclusão de dados do usuário
- Expotação de dados dos usuários
- Importação de dados dos usuários

  ## Fluxo do Processo:
- Criação do repositório
- Criação da branch develop
- Criação da branch stage
- Criação da branch feature/cadastro e desenvolvimento do código nela
- Criação da branch feature/consulta e desenvolvimento do código nela
- Criação da branch feature/expotação e desenvolvimento do código neala
- Após finalização do código, fazer o push para cada branch origin(remota) do código
- Fazer pull request da branch origin de cada código para a develop
- Verificação e aprovação de cada pull request e por fim merge
- Repete o fluxo da develop para stage e da stage para main(produção)

## Regras de negócio:
- Cada desenvolvedor só pode trabalhar em sua própria branch
- Cada pull request precisa ser revisado por ao menos um outro dev e um bot code review
- É preciso seguir o fluxo de develop, stage e por fim Main
- Regra de commit, <tipo(#issue): descrição do commit>

## Exceções:
- Conflito no código atual e antigo
- Comentário do commit fora do padrão
- Código incorreto ou que apresenta uma possível vulnerabilidade

## Pré-condições:
- Git e Github configurados
- Equipe definida
- Branchs padrões criadas
- Editor de código instalado e configurado

## Ambiente de desenvolvimento:
- O desenvolvimento é feito por meio de editores de código e ferramentas de versionamento.
### Ferramentas utilizadas:
- Linguagem de programação: Python
- Software de versionamento local: Git
- Saas de versionamento: Github
- Editor de código: VS code

## Estrutura do repositório:
- Main: código de produção
- Develop: código de desenvolvimento
- Stage: Código onde são feito os testes

## Estrutura de Processo:
- Versionamento com Git
- Organização em branches (GitFlow)
- Integração via Pull Request
- Revisão de código (code review

## Versionamento do git usando gitflow
- Main -> develop -> criação da feature(ou fix) apartir da develop -> git add -> git commit -> git push -> pull request da feature... para develop -> merge -> pull request develop para stage -> merge -> pull request stage para Main.
