
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Coleta Centro", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: white;'>Dashboard - Coleta Centro</h1>",
    unsafe_allow_html=True
)

# Ler os dados
df = pd.read_excel("Coleta centro.xlsx")

# Limpeza de dados
df = df.fillna(0)
df = df[df["Mês"].notna() & (df["Mês"] != "Total")]

# Sidebar para seleção de mês
meses = df["Mês"].tolist()
mes = st.sidebar.selectbox("Selecione o mês", meses + ["Todos"])

if mes != "Todos":
    dados = df[df["Mês"] == mes]
else:
    dados = df

# KPIs
coleta_am = dados["Coleta AM"].sum()
coleta_pm = dados["Coleta PM"].sum()
total = dados["Total"].sum()

st.markdown("##")
kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(label="Manhã (kg)", value=f"{coleta_am:,.0f}")
kpi2.metric(label="Tarde (kg)", value=f"{coleta_pm:,.0f}")
kpi3.metric(label="Total (kg)", value=f"{total:,.0f}")

# Gráfico de barras
st.markdown("### Distribuição por Período")
fig_bar = px.bar(
    dados,
    x=["Coleta AM", "Coleta PM"],
    y="Mês",
    orientation="h",
    title="Coleta por Período",
    labels={"value": "Quantidade (kg)", "Mês": "Mês", "variable": "Período"},
    color_discrete_sequence=["#00FFFF", "#FF6600"]
)
fig_bar.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font_color="white"
)
st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de pizza
st.markdown("### Proporção Manhã vs Tarde")
fig_pie = px.pie(
    names=["Manhã", "Tarde"],
    values=[coleta_am, coleta_pm],
    title="Distribuição Total",
    color_discrete_sequence=["#00FFFF", "#FF6600"]
)
fig_pie.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font_color="white"
)
st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")
st.caption("Projeto Zeladoria - Coleta Centro")
