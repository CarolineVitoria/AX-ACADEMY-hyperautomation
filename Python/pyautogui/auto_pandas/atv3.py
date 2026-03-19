import pandas as pd
import numpy as np


np.random.seed(42)

n = 50

df = pd.DataFrame({
    "Pedido_ID": range(1, n+1),
    "Cliente": np.random.choice(
        ["Empresa A", "Empresa B", "Empresa C", "Empresa D", "Empresa E"], n
    ),
    "Status": np.random.choice(
        ["Aprovado", "Revisao"], n, p=[0.7, 0.3]
    ),
    "Total_Liquido": np.random.uniform(200, 50000, n).round(2)
})

def classificar_cat(v):
    if v > 2000:
        return "Grande"
    elif v >1001:
        return "Médio"
    else:
        return "Pequeno"

df["Categoria"]= df["Total_Liquido"].apply(classificar_cat)

def exportar_relatorio(df):
    df.to_excel("rel_pedidos.xlsx", index=False)
    resumo = (
        df.groupby("Status").agg(
            Quantida_pd=("Pedido_ID", "count"),
            Total_L=("Total_Liquido", "sum")
        )
    )
    
    print("Resumo por Status: ")
    print(resumo)

exportar_relatorio(df)