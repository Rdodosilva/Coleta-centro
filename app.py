
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Coleta Futurista", layout="centered", page_icon="🚛")

st.markdown("""
    <style>
        body { background-color: #0e1117; color: white; }
        .stApp { background: #0e1117; }
        h1, h2, h3, h4 { color: #00b4d8; }
    </style>
""", unsafe_allow_html=True)

st.title("🚛 Dashboard Futurista - Coleta de Resíduos (Centro)")

df = pd.read_csv("dados_coleta_kg.csv")
meses = df["Mes"].unique().tolist()
mes_escolhido = st.selectbox("Escolha o mês:", meses)

filtro = df[df["Mes"] == mes_escolhido].iloc[0]
manha = int(filtro["Coleta_AM_kg"])
tarde = int(filtro["Coleta_PM_kg"])
total = int(filtro["Total_kg"])

col1, col2, col3 = st.columns(3)
col1.metric("🌅 Manhã (kg)", f"{manha:,}", help="20kg por saco")
col2.metric("🌇 Tarde (kg)", f"{tarde:,}", help="20kg por saco")
col3.metric("🧮 Total do mês", f"{total:,}", help="Somatório total")

# Gráfico de barras
df_bar = pd.DataFrame({
    "Período": ["Manhã", "Tarde"],
    "Kg": [manha, tarde]
})
fig_bar = px.bar(df_bar, x="Período", y="Kg", color="Período",
                 color_discrete_map={"Manhã": "#00b4d8", "Tarde": "#f77f00"},
                 title=f"Distribuição de Coleta - {mes_escolhido}",
                 height=400)
st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de pizza
fig_pie = px.pie(df_bar, names="Período", values="Kg", hole=0.5,
                 color="Período", color_discrete_map={"Manhã": "#00b4d8", "Tarde": "#f77f00"})
st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("🚀 Desenvolvido por [Seu Nome] - Projeto Zeladoria Centro")
