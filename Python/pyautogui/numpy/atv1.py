import numpy as np
import pandas as pd

np.random.seed(7)

n = 200

df = pd.DataFrame({
    'id': np.arange(1, n + 1),
    'data': pd.date_range('2026-02-01', periods=n, freq='D').astype(str),
    'valor': np.round(np.random.normal(loc=200.0, scale=80.0, size=n), 2),
    'taxa': np.round(
        np.random.choice([0.0, 0.05, 0.1, 0.15], size=n,
                         p=[0.2, 0.4, 0.3, 0.1]), 2)
})

df['total'] = np.round(df['valor'] * (1 + df['taxa']), 2)


idx_na = np.random.choice(n, 6, replace=False)
df.loc[idx_na, 'taxa'] = np.nan

idx_err = np.random.choice(n, 10, replace=False)
df.loc[idx_err, 'total'] = (
    df.loc[idx_err, 'total'] +
    np.random.choice([5, -7, 12], size=10)
)

df['total_calc'] = np.round(
    df['valor'] * (1.0 + np.nan_to_num(df['taxa'], nan=0.0)), 2
)


m_taxa_falta = np.isnan(df['taxa'])

m_taxa_fora = (df['taxa'] < 0) | (df['taxa'] > 0.15)

m_total_div = np.abs(df['total_calc'] - df['total']) > 0.01


df['taxa_valida'] = ~(m_taxa_falta | m_taxa_fora)


motivo = np.full(len(df), '', dtype=object)

motivo = np.where(m_taxa_falta, motivo + 'taxa_faltando; ', motivo)
motivo = np.where(m_taxa_fora, motivo + 'taxa_fora_faixa; ', motivo)
motivo = np.where(m_total_div, motivo + 'total_diverge; ', motivo)

df['motivo'] = motivo


m_excecao = m_taxa_falta | m_taxa_fora | m_total_div

relatorio_excecoes = df[m_excecao]


relatorio_taxa_fora = df[m_taxa_fora]



df.to_csv("base_completa.csv", index=False)

relatorio_excecoes.to_csv(
    "relatorio_excecoes.csv",
    index=False
)

relatorio_taxa_fora.to_csv(
    "relatorio_taxa_fora_faixa.csv",
    index=False
)
print(df)
print("Arquivos gerados com sucesso!")