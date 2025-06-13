
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Coleta Centro - Visual Neon", layout="wide")

st.markdown("""
    <style>
        body { background-color: #0e0e2c; }
        .stApp {
            background-color: #0e0e2c;
            color: white;
        }
        h1, h2, h3 {
            color: #8a2be2;
        }
        .block-container {
            padding-top: 2rem;
        }
        .metric {
            background: #1f1f3a;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #e600ff;'>🚛 Coleta Centro - Dashboard Neon</h1>", unsafe_allow_html=True)

df = pd.read_csv("dados_coleta_kg.csv")
meses = df["Mes"].unique().tolist()
mes_escolhido = st.selectbox("🗓️ Selecione o mês:", meses)

filtro = df[df["Mes"] == mes_escolhido].iloc[0]
manha = int(filtro["Coleta_AM_kg"])
tarde = int(filtro["Coleta_PM_kg"])
total = int(filtro["Total_kg"])

col1, col2, col3 = st.columns(3)
col1.metric("🌅 Manhã (kg)", f"{manha:,}", help="Coleta média: 20kg por saco")
col2.metric("🌇 Tarde (kg)", f"{tarde:,}", help="Coleta média: 20kg por saco")
col3.metric("🧮 Total Mensal", f"{total:,}")

# Gráfico de barras horizontal
df_bar = pd.DataFrame({
    "Período": ["Manhã", "Tarde"],
    "Kg": [manha, tarde]
})
fig_bar = px.bar(df_bar, y="Período", x="Kg", orientation="h", color="Período",
                 color_discrete_map={"Manhã": "#00f2ff", "Tarde": "#ff6a00"},
                 title=f"Distribuição por Período - {mes_escolhido}",
                 height=400)
fig_bar.update_layout(
    paper_bgcolor="#0e0e2c",
    plot_bgcolor="#0e0e2c",
    font_color="white"
)
st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de pizza
fig_pie = px.pie(df_bar, names="Período", values="Kg", hole=0.45,
                 color="Período", color_discrete_map={"Manhã": "#00f2ff", "Tarde": "#ff6a00"})
fig_pie.update_layout(
    paper_bgcolor="#0e0e2c",
    font_color="white",
    legend_font_color="white"
)
st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>🔮 Desenvolvido com visual neon para análise de coleta inteligente</p>", unsafe_allow_html=True)
