import plotly.express as px

def gerar_grafico_pizza(df_filtrado):
    df_despesas = df_filtrado[df_filtrado["Tipo"] == "Despesa"]
    if not df_despesas.empty:
        df_pizza = df_despesas.groupby("Categoria")["Valor"].sum().abs().reset_index()
        fig = px.pie(df_pizza, values="Valor", names="Categoria", hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        return fig
    return None

def gerar_grafico_linha(df_filtrado):
    df_linha = df_filtrado.sort_values(by="Data")
    df_linha["Saldo Acumulado"] = df_linha["Valor"].cumsum()
    fig = px.line(df_linha, x="Data", y="Saldo Acumulado", markers=True,
                  labels={"Saldo Acumulado": "Saldo (R$)"})
    return fig