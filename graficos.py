import plotly.express as px

def gerar_grafico_pizza(df_filtrado):
    df_despesas = df_filtrado[df_filtrado["Tipo"] == "Despesa"]
    if not df_despesas.empty:
        # Agrupa e soma os gastos por categoria
        df_pizza = df_despesas.groupby("Categoria")["Valor"].sum().abs().reset_index()
        
        # 1. Criamos o gráfico base (aqui aumentamos o furo central de 0.4 para 0.6)
        fig = px.pie(
            df_pizza, 
            values="Valor", 
            names="Categoria", 
            hole=0.6, # Transforma em gráfico de rosca mais fino/elegante
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        # 2. Adicionamos as configurações avançadas de animação e design
        fig.update_traces(
            textinfo="percent+label",     # Mostra o nome e a % direto na rosca
            pull=[0.05] * len(df_pizza),  # Faz TODAS as fatias ficarem levemente separadas (efeito "explode")
            hoverinfo="label+value+percent", 
            hole=0.6
        )
        
        # 3. Ajustamos o layout para ativar animações ao carregar
        fig.update_layout(
            showlegend=False, # Esconde a legenda lateral (já que o nome está na fatia)
            margin=dict(t=20, b=20, l=20, r=20), # Remove margens sobrando
            transition_duration=500 # Adiciona uma animação suave de 500ms ao carregar/filtrar
        )
        
        return fig
    return None

def gerar_grafico_linha(df_filtrado):
    df_linha = df_filtrado.sort_values(by="Data")
    df_linha["Saldo Acumulado"] = df_linha["Valor"].cumsum()
    fig = px.line(df_linha, x="Data", y="Saldo Acumulado", markers=True,
                  labels={"Saldo Acumulado": "Saldo (R$)"})
    
    # Bônus: adicionando animação suave de transição também no gráfico de linha
    fig.update_layout(transition_duration=500)
    return fig