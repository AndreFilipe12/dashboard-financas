# 💰 Dashboard de Finanças Pessoais com Consultor Virtual

Controle financeiro pessoal construído em **Python** utilizando a biblioteca **Streamlit**. O sistema permite gerenciar transações (receitas e despesas), definir orçamentos mensais dinâmicos por categoria e receber conselhos financeiros estratégicos gerados 
por um consultor virtual integrado.

---

## 🚀 Funcionalidades Principais

* **📈 Dashboard Interativo:** Visualização de métricas chave (Total de Receitas, Despesas e Saldo do Período) com filtros de ano e mês.
* **🎯 Gestão de Metas e Orçamentos:** Interface visual na barra lateral para estipular limites de gastos mensais por categoria, com barras de progresso que alertam o usuário caso o limite esteja próximo ou tenha sido estourado.
* **💡 Consultor Virtual de Insights:** Módulo inteligente local que analisa a saúde financeira atual do usuário e exibe avisos automáticos sobre o maior vilão de gastos e a taxa de poupança.
* **📊 Gráficos Modernos:** Gráfico de rosca (*Donut Chart*) animado com efeito de explosão para distribuição de despesas por categoria e gráfico de linha para evolução do saldo acumulado.
* **🗑️ Histórico e Remoção:** Tabela de transações com ordenação automática e sistema integrado para deletar registros incorretos diretamente pela interface.
* **📥 Exportação de Dados:** Opção para baixar o extrato filtrado atual diretamente no formato `.csv`.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Streamlit** (Interface Web e Componentes)
* **Pandas** (Estruturação, filtragem e manipulação de dados)
* **Plotly Express** (Gráficos dinâmicos e animações de transição)

---

## 📦 Estrutura do Projeto

O projeto adota boas práticas de mercado com uma arquitetura **modular**, dividindo as responsabilidades em arquivos separados:

```text
dashboard_finanças/
│
├── app.py           # Arquivo principal (Interface Visual e Lógica de Insights)
├── backend.py       # Manipulação de arquivos, persistência de dados e metas (.json/.csv)
├── graficos.py      # Configuração e renderização dos gráficos com Plotly
├── .gitignore       # Proteção para não subir arquivos de dados pessoais
└── README.md        # Documentação do projeto
```
🔧 Como Executar o Projeto Localmente

git clone [https://github.com/AndreFilipe12/dashboard-financas.git](https://github.com/AndreFilipe12/dashboard-financas.git)
cd dashboard-financas

🛠️ Dependências
Para executar este projeto, precisas do Python 3 instalado e das seguintes bibliotecas:
* **pip install streamlit pandas plotly**

▶️Rodar a Aplicação
Executa o comando do Streamlit para abrir o dashboard no teu navegador:
* **streamlit run app.py**
