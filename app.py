import streamlit as st
import pandas as pd
from datetime import datetime

# Importações dos módulos que criámos
import backend
import graficos

st.set_page_config(page_title="Minhas Finanças", layout="wide")
st.title("💰 Dashboard de Finanças Pessoais")

df = backend.carregar_dados()

# --- ABA DE ENTRADA DE DADOS (Barra Lateral) ---
st.sidebar.header("📝 Nova Transação")
with st.sidebar.form(key="form_transacao", clear_on_submit=True):
    data = st.date_input("Data", datetime.now())
    descricao = st.text_input("Descrição (Ex: Supermercado, Salário)")
    categoria = st.selectbox("Categoria", ["Alimentação", "Moradia", "Transporte", "Lazer", "Salário", "Investimentos", "Outros"])
    tipo = st.selectbox("Tipo", ["Despesa", "Receita"])
    valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01)
    botao_salvar = st.form_submit_button("Salvar Transação")

if botao_salvar and descricao:
    df = backend.salvar_transacao(df, data, descricao, categoria, tipo, valor)
    st.sidebar.success("Transação salva!")
    st.rerun()

# --- ABA DE ELIMINAR TRANSAÇÃO (Barra Lateral) ---
if not df.empty:
    st.sidebar.markdown("---")
    st.sidebar.header("🗑️ Eliminar Transação")
    
    opcoes_eliminar = {}
    for idx, row in df.iterrows():
        data_formatada = row["Data"].strftime("%Y-%m-%d")
        texto_opcao = f"{data_formatada} | {row['Descrição']}: R$ {row['Valor']:.2f}"
        opcoes_eliminar[texto_opcao] = idx
        
    opcao_selecionada = st.sidebar.selectbox("Escolha para apagar:", list(opcoes_eliminar.keys()))
    
    if st.sidebar.button("❌ Apagar Selecionada", use_container_width=True):
        indice_alvo = opcoes_eliminar[opcao_selecionada]
        df = backend.eliminar_transacao(df, indice_alvo)
        st.sidebar.error("Transação removida!")
        st.rerun()

# --- ABA DE FILTROS (Barra Lateral) ---
st.sidebar.markdown("---")
st.sidebar.header("🔍 Filtros")

if not df.empty:
    df["Ano"] = df["Data"].dt.year
    df["Mês"] = df["Data"].dt.strftime("%m - %B")
    
    anos_disponiveis = sorted(df["Ano"].unique(), reverse=True)
    ano_selecionado = st.sidebar.selectbox("Selecione o Ano", anos_disponiveis)
    
    meses_disponiveis = sorted(df[df["Ano"] == ano_selecionado]["Mês"].unique())
    meses_disponiveis.insert(0, "Todos os Meses")
    mes_selecionado = st.sidebar.selectbox("Selecione o Mês", meses_disponiveis)
    
    df_filtrado = df[df["Ano"] == ano_selecionado]
    if mes_selecionado != "Todos os Meses":
        df_filtrado = df_filtrado[df_filtrado["Mês"] == mes_selecionado]
else:
    df_filtrado = df

# --- EXIBIÇÃO DO DASHBOARD ---
if not df_filtrado.empty:
    receitas = df_filtrado[df_filtrado["Tipo"] == "Receita"]["Valor"].sum()
    despesas = df_filtrado[df_filtrado["Tipo"] == "Despesa"]["Valor"].sum()
    saldo_atual = receitas + despesas
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Receitas", value=f"R$ {receitas:.2f}", delta_color="normal")
    col2.metric(label="Total Despesas", value=f"R$ {abs(despesas):.2f}", delta_color="inverse")
    col3.metric(label="Saldo do Período", value=f"R$ {saldo_atual:.2f}")
    
    st.markdown("---")
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.subheader("Despesas por Categoria")
        fig_pizza = graficos.gerar_grafico_pizza(df_filtrado)
        if fig_pizza:
            st.plotly_chart(fig_pizza, use_container_width=True)
        else:
            st.info("Nenhuma despesa no período.")
            
    with col_graf2:
        st.subheader("Evolução do Saldo no Tempo")
        fig_linha = graficos.gerar_grafico_linha(df_filtrado)
        st.plotly_chart(fig_linha, use_container_width=True)

        # --- SISTEMA DE ALERTAS DE ORÇAMENTO ---
    st.subheader("🎯 Metas e Orçamentos do Mês Atual")
    status_metas = backend.calcular_orcamentos(df)
    
    if status_metas:
        # Cria colunas dinâmicas na tela para colocar as barras lado a lado
        cols_metas = st.columns(len(status_metas))
        
        for i, (categoria, dados) in enumerate(status_metas.items()):
            with cols_metas[i]:
                st.caption(f"**{categoria}**")
                st.text(f"R$ {dados['gasto']:.2f} / R$ {dados['limite']:.2f}")
                
                # Exibe a barra de progresso
                st.progress(dados["porcentagem"])
                
                # Alertas visuais com base no consumo
                if dados["gasto"] > dados["limite"]:
                    st.error("🚨 Limite Estourado!")
                elif dados["gasto"] >= dados["limite"] * 0.8:
                    st.warning("⚠️ Atenção! Gasto alto.")
                else:
                    st.success("✅ Dentro da meta")

    st.markdown("---")
    
    col_tabela, col_exportar = st.columns([4, 1])
    with col_tabela:
        st.subheader("Histórico de Transações Filtradas")
    with col_exportar:
        csv_data = df_filtrado[["Data", "Descrição", "Categoria", "Tipo", "Valor"]].to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Exportar para CSV", data=csv_data, file_name="extrato.csv", mime="text/csv")
    
    df_exibicao = df_filtrado[["Data", "Descrição", "Categoria", "Tipo", "Valor"]].copy()
    df_exibicao["Data"] = df_exibicao["Data"].dt.strftime("%Y-%m-%d")
    st.dataframe(df_exibicao.sort_values(by="Data", ascending=False), use_container_width=True)
else:
    st.info("Banco de dados vazio ou sem dados para os filtros selecionados.")