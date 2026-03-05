import pandas as pd
import numpy as np
import re

logs = """
2026-02-21 10:15:07 | ERROR | user=lucas | Falha ao abrir o site | tel=+55 (92) 99999-1234 | total=R$ 1.234,56 | email=lucas@empresa.com
2026-02-21 10:16:10 | INFO  | user=ana   | Login realizado      | tel=(92)9999-1234     | total=R$ 10,00     | email=ana.silva@empresa.com.br
2026-02-21 10:17:01 | WARN  | user=lucas | Timeout na API externa | tel=92999991234 | total=R$ 0,99 | email=suporte@site.co
linha errada sem padrão
2026-02-21 10:18:55 | ERROR | user=ana | Falha ao salvar arquivo | tel=abc | total=R$ 25,50 | email=ana@@site.org
2026-02-21 10:20:00 | INFO | user=joao | Logout | total=R$ 7,00
"""
#print(logs)
#o re compiler melhora a organização, reutulização e código limpo
#o re.verbose permite escrever regex mult linhas
padrao = re.compile(r"""
                    ^
                    (?P<data>\d{4}\-\d{2}-\d{2})\s+
                    (?P<hora>\d{2}:\d{2}:\d{2})\s+\|\s+
                    (?P<tipo_log>(ERROR|INFO|WARN))\s+\|\s+
                    (user=)(?P<usuario>[\w\s]+)\s+\|\s+
                    (?P<informacao>[^|]+)\s+\|\s+
                    (tel=)(?P<celular>[^|]+)\s+\|\s+
                    (total=)(?P<TOTAL>R\$\s*[\d.,]+)\s+\|\s+
                    (email=)(?P<Email>[^|]+)\s*
                    $
                    """, flags=re.VERBOSE | re.MULTILINE)

lista_logs = []
# extração e limpeza básica
for match in padrao.finditer(logs):
    #print("Teste groupDict: ", match["tipo_log"])
    log_dic = match.groupdict()
    for k in ("informacao", "celular", "email", "total"):
        if log_dic.get(k) is not None:
            log_dic[k] = log_dic[k].strip() #tira os espaões em branco
    lista_logs.append(log_dic)


print(lista_logs)


# contabilização dos registros obtidos
#o strip() retira os espaços do início e fim da string, splitlines() pega cada string separada por quebra de linha
#e tranforma em um elemento de uma lista

linhas = [l for l in logs.strip().splitlines() if l.strip()] # aqui fazendo uma lsita comprehesion
print(f"Linhas originias: {len(linhas)}")
print(f"Registros obtidos: {len(lista_logs)}")
print(f"Linhas ignoradas: {len(linhas)-len(lista_logs)}")

#Limpeza e normalização dos dados
#limpeza de espaços, telefone apenas com dígitos, e padronizar com ddi 55 quando possível
#utilizar o re.sub, re.sub(padrao, substituicao, string)
#adcionar o 55 apenas se o número tiver 10 ou 11

def padronizacaoCelular(cel):
    cel = re.sub(r"\D+", "", cel)
    print("dps de retirar os não dígitos", cel)
    print(len(cel))
    if len(cel) == 10 | len(cel) == 11:
        cel = "55"+cel
        print("Após adcionar", cel)
    return cel

for r in lista_logs:
    r["celular"] = padronizacaoCelular(r.get("celular"))

print(lista_logs)