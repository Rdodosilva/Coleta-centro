import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Coleta Centro", layout="wide")

# Dados
dados = {
    "Mês": ["Janeiro", "Fevereiro", "Março", "Abril", "Maio"],
    "Coleta AM": [295, 1021, 408, 1192, 1045],
    "Coleta PM": [760, 1636, 793, 1606, 1461]
}
df = pd.DataFrame(dados)
df["Total"] = df["Coleta AM"] + df["Coleta PM"]
df["Coleta AM (kg)"] = df["Coleta AM"] * 20
df["Coleta PM (kg)"] = df["Coleta PM"] * 20
df["Total (kg)"] = df["Total"] * 20

st.markdown("<h1 style='text-align: center; color: white;'>Coleta Centro</h1>", unsafe_allow_html=True)

# Seleção de mês
mes = st.selectbox("Selecione o mês:", df["Mês"].tolist())

# Dados do mês selecionado
dados_mes = df[df["Mês"] == mes].iloc[0]

# Métricas
col1, col2, col3 = st.columns(3)
col1.metric("🌅 Manhã (kg)", f"{dados_mes['Coleta AM (kg)']:,}".replace(",", "."))
col2.metric("🌇 Tarde (kg)", f"{dados_mes['Coleta PM (kg)']:,}".replace(",", "."))
col3.metric("📋 Total Mensal", f"{dados_mes['Total (kg)']:,}".replace(",", "."))

# Gráfico de barras
df_bar = pd.DataFrame({
    "Período": ["Manhã", "Tarde"],
    "Peso (kg)": [dados_mes["Coleta AM (kg)"], dados_mes["Coleta PM (kg)"]]
})

st.subheader(f"Distribuição por Período - {mes}")
fig_bar = px.bar(
    df_bar,
    x="Peso (kg)",
    y="Período",
    orientation="h",
    color="Período",
    color_discrete_map={"Manhã": "deepskyblue", "Tarde": "darkorange"},
    text="Peso (kg)"
)
fig_bar.update_layout(
    paper_bgcolor="#0a0a19",
    plot_bgcolor="#0a0a19",
    font=dict(color="white")
)
st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de pizza com total geral
st.subheader("Distribuição da Coleta Total")
df_total = pd.DataFrame({
    "Período": ["Manhã", "Tarde"],
    "Peso (kg)": [df["Coleta AM (kg)"].sum(), df["Coleta PM (kg)"].sum()]
})
fig_pie = px.pie(
    df_total,
    names="Período",
    values="Peso (kg)",
    color="Período",
    color_discrete_map={"Manhã": "deepskyblue", "Tarde": "darkorange"},
    hole=0.4
)
fig_pie.update_layout(
    paper_bgcolor="rgb(10,10,25)",
    plot_bgcolor="rgb(10,10,25)",
    font=dict(color="white")
)
st.plotly_chart(fig_pie, use_container_width=True)
