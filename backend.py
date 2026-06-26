import pandas as pd
import os

ARQUIVO_DADOS = "financeiro.csv"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        dados = pd.read_csv(ARQUIVO_DADOS)
        dados["Data"] = pd.to_datetime(dados["Data"])
        return dados
    else:
        return pd.DataFrame(columns=["Data", "Descrição", "Categoria", "Tipo", "Valor"])

def salvar_transacao(df, data, descricao, categoria, tipo, valor):
    nova_linha = {
        "Data": pd.to_datetime(data),
        "Descrição": descricao,
        "Categoria": categoria,
        "Tipo": tipo,
        "Valor": valor if tipo == "Receita" else -valor
    }
    df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
    df.to_csv(ARQUIVO_DADOS, index=False)
    return df

def eliminar_transacao(df, indice):
    df = df.drop(indice)
    df.to_csv(ARQUIVO_DADOS, index=False)
    return df

def calcular_orcamentos(df):
    # Dicionário onde você define seus limites mensais por categoria (mude os valores como quiser!)
    limites = {
        "Alimentação": 500.00,
        "Moradia": 1200.00,
        "Transporte": 300.00,
        "Lazer": 400.00,
        "Outros": 250.00
    }
    
    status_orcamento = {}
    
    if not df.empty:
        # Filtra apenas despesas do mês e ano atuais
        hoje = pd.Timestamp.now()
        df_mes_atual = df[(df["Tipo"] == "Despesa") & 
                          (df["Data"].dt.month == hoje.month) & 
                          (df["Data"].dt.year == hoje.year)]
        
        # Calcula o total gasto por categoria no mês
        gastos_por_cat = df_mes_atual.groupby("Categoria")["Valor"].sum().abs()
        
        for categoria, limite in limites.items():
            gasto_atual = gastos_por_cat.get(categoria, 0.0)
            status_orcamento[categoria] = {
                "gasto": gasto_atual,
                "limite": limite,
                "porcentagem": min(gasto_atual / limite, 1.0) if limite > 0 else 0.0
            }
            
    return status_orcamento