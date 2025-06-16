import streamlit as st
import pandas as pd
import plotly.express as px

# 🔥 Configuração da página
st.set_page_config(
    page_title="Dashboard Coleta Centro",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    body {
        background-color: #0a0a19;
        color: white;
    }
    .stApp {
        background-color: #0a0a19;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: white;'>📦 Dashboard - Coleta Centro</h1>", unsafe_allow_html=True)

# 📥 Carregar os dados
df = pd.read_excel("Coleta_centro2.xlsx")

# 🔧 Processamento
df["Data"] = pd.to_datetime(df["Data"])
df["Mês"] = df["Data"].dt.strftime('%B').str.capitalize()
df["Peso (kg)"] = df["Sacos Coletados"] * 20

# 🎯 Filtros
meses = sorted(df["Mês"].unique(), key=lambda x: pd.to_datetime(x, format='%B').month)
mes_selecionado = st.sidebar.selectbox("Selecione o mês:", meses)

df_filtrado = df[df["Mês"] == mes_selecionado]

# 📊 KPIs
total_manha = df_filtrado[df_filtrado["Período"] == "Manhã"]["Peso (kg)"].sum()
total_tarde = df_filtrado[df_filtrado["Período"] == "Tarde"]["Peso (kg)"].sum()
total_geral = total_manha + total_tarde

col1, col2, col3 = st.columns(3)
col1.metric("🌅 Manhã (kg)", f"{total_manha:,.0f}".replace(",", "."))
col2.metric("🌇 Tarde (kg)", f"{total_tarde:,.0f}".replace(",", "."))
col3.metric("📋 Total (kg)", f"{total_geral:,.0f}".replace(",", "."))

st.markdown("---")

# 📈 Gráfico de Barras - Coleta por Dia no mês selecionado
st.subheader(f"Coleta por Dia - {mes_selecionado}")
df_grouped = df_filtrado.groupby(["Data", "Período"])["Peso (kg)"].sum().reset_index()

fig_bar = px.bar(
    df_grouped,
    x="Data",
    y="Peso (kg)",
    color="Período",
    barmode="group",
    color_discrete_map={"Manhã": "deepskyblue", "Tarde": "darkorange"},
    title=f"Coleta por Dia em {mes_selecionado}"
)
fig_bar.update_layout(
    paper_bgcolor="#0a0a19",
    plot_bgcolor="#0a0a19",
    font_color="white"
)
st.plotly_chart(fig_bar, use_container_width=True)

# 🥧 Gráfico de Pizza - Manhã vs Tarde no mês selecionado
st.subheader(f"Distribuição Manhã x Tarde - {mes_selecionado}")
fig_pie = px.pie(
    names=["Manhã", "Tarde"],
    values=[total_manha, total_tarde],
    color=["Manhã", "Tarde"],
    color_discrete_map={"Manhã": "deepskyblue", "Tarde": "darkorange"},
    hole=0.4
)
fig_pie.update_layout(
    paper_bgcolor="#0a0a19",
    plot_bgcolor="#0a0a19",
    font_color="white"
)
st.plotly_chart(fig_pie, use_container_width=True)

# 🔥 Gráfico de Barras Geral por mês
st.subheader("Comparativo Geral por Mês")
df_mes = df.groupby(["Mês", "Período"])["Peso (kg)"].sum().reset_index()
fig_bar_mes = px.bar(
    df_mes,
    x="Mês",
    y="Peso (kg)",
    color="Período",
    barmode="group",
    category_orders={"Mês": meses},
    color_discrete_map={"Manhã": "deepskyblue", "Tarde": "darkorange"},
    title="Coleta Geral por Mês"
)
fig_bar_mes.update_layout(
    paper_bgcolor="#0a0a19",
    plot_bgcolor="#0a0a19",
    font_color="white"
)
st.plotly_chart(fig_bar_mes, use_container_width=True)

