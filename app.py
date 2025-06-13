import streamlit as st
import pandas as pd
import plotly.express as px

# Estilo da página
st.set_page_config(layout="wide", page_title="Coleta Centro - Dashboard Neon")

# Carregar dados
@st.cache_data
def load_data():
    data = {
        "Mês": ["Janeiro", "Fevereiro", "Março", "Abril", "Maio"],
        "Coleta AM": [295, 1021, 408, 1192, 1045],
        "Coleta PM": [760, 1636, 793, 1606, 1461]
    }
    df = pd.DataFrame(data)
    df["Total"] = df["Coleta AM"] + df["Coleta PM"]
    df["Coleta AM (kg)"] = df["Coleta AM"] * 20
    df["Coleta PM (kg)"] = df["Coleta PM"] * 20
    df["Total (kg)"] = df["Total"] * 20
    return df

df = load_data()

# Tema e título
st.markdown("<h1 style='color:white; text-align: center;'>Coleta Centro</h1>", unsafe_allow_html=True)
st.markdown("###", unsafe_allow_html=True)

# Filtro de mês
meses = df["Mês"].tolist()
mes_selecionado = st.selectbox("Selecione o mês:", meses)

# Filtrar dados
df_filtrado = df[df["Mês"] == mes_selecionado]

# Métricas
col1, col2, col3 = st.columns(3)
col1.metric("🌅 Manhã (kg)", f'{df_filtrado["Coleta AM (kg)"].values[0]:,.0f}')
col2.metric("🌇 Tarde (kg)", f'{df_filtrado["Coleta PM (kg)"].values[0]:,.0f}')
col3.metric("📅 Total Mensal", f'{df_filtrado["Total (kg)"].values[0]:,.0f}')

# Gráfico
st.markdown(f"### Distribuição por Período - {mes_selecionado}")
df_plot = pd.DataFrame({
    "Período": ["Manhã", "Tarde"],
    "KG": [df_filtrado["Coleta AM (kg)"].values[0], df_filtrado["Coleta PM (kg)"].values[0]]
})
colors = {"Manhã": "#00FFFF", "Tarde": "#FF6A00"}
fig = px.bar(df_plot, x="KG", y="Período", color="Período", orientation="h", color_discrete_map=colors)
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)
st.plotly_chart(fig, use_container_width=True)