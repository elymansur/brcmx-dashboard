import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from io import BytesIO

st.set_page_config(layout="wide")
st.image("dashboard/logo_brcmx.png", width=200)
st.title("📦 Plataforma de Comércio Exterior - BRCMX")

# 🔓 LOGIN DESATIVADO TEMPORARIAMENTE

# Conexão com PostgreSQL
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

@st.cache_data
def carregar_dados():
    engine = create_engine(DATABASE_URL)
    df = pd.read_sql("SELECT * FROM movimentacoes", engine)
    return df

df = carregar_dados()

# Filtros
st.sidebar.header("🔎 Filtros")
anos = st.sidebar.multiselect("Ano", options=sorted(df["ano"].unique()), default=None)
fluxos = st.sidebar.multiselect("Tipo de Fluxo", options=sorted(df["tipo_fluxo"].dropna().unique()), default=["exportacao"])
ufs = st.sidebar.multiselect("UF", options=sorted(df["uf"].dropna().unique()), default=None)
paises = st.sidebar.multiselect("País", options=sorted(df["pais"].dropna().unique()), default=None)
ncm_codes = st.sidebar.multiselect("NCM", options=sorted(df["ncm"].dropna().unique()), default=None)
meses = st.sidebar.multiselect("Mês", options=sorted(df["mes"].dropna().unique()), default=None)

st.sidebar.markdown("---")
valor_min, valor_max = float(df["valor_fob"].min()), float(df["valor_fob"].max())
fob_range = st.sidebar.slider("Valor FOB (US$)", min_value=valor_min, max_value=valor_max,
                              value=(valor_min, valor_max), step=1000.0)

peso_min, peso_max = float(df["peso_liquido"].min()), float(df["peso_liquido"].max())
peso_range = st.sidebar.slider("Peso Líquido (kg)", min_value=peso_min, max_value=peso_max,
                               value=(peso_min, peso_max), step=100.0)

search_ncm = st.sidebar.text_input("Buscar por descrição NCM", "")

df_filtrado = df.copy()
if anos:
    df_filtrado = df_filtrado[df_filtrado["ano"].isin(anos)]
if fluxos:
    df_filtrado = df_filtrado[df_filtrado["tipo_fluxo"].isin(fluxos)]
if ufs:
    df_filtrado = df_filtrado[df_filtrado["uf"].isin(ufs)]
if paises:
    df_filtrado = df_filtrado[df_filtrado["pais"].isin(paises)]
if ncm_codes:
    df_filtrado = df_filtrado[df_filtrado["ncm"].isin(ncm_codes)]
if meses:
    df_filtrado = df_filtrado[df_filtrado["mes"].isin(meses)]

df_filtrado = df_filtrado[
    (df_filtrado["valor_fob"] >= fob_range[0]) &
    (df_filtrado["valor_fob"] <= fob_range[1]) &
    (df_filtrado["peso_liquido"] >= peso_range[0]) &
    (df_filtrado["peso_liquido"] <= peso_range[1])
]
if search_ncm:
    df_filtrado = df_filtrado[df_filtrado["descricao_ncm"].str.contains(search_ncm, case=False, na=False)]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Valor FOB Total (US$)", f"{df_filtrado['valor_fob'].sum():,.0f}")
col2.metric("Peso Líquido Total (kg)", f"{df_filtrado['peso_liquido'].sum():,.0f}")
col3.metric("Qtd Registros", f"{len(df_filtrado):,}")

# Exportação Excel
st.markdown("### 📥 Exportar Dados")
buffer = BytesIO()
df_filtrado.to_excel(buffer, index=False)
st.download_button("⬇️ Baixar Excel (.xlsx)", data=buffer.getvalue(), file_name="dados_exportados.xlsx")

# Gráficos
st.markdown("## 📊 Gráficos Analíticos")

fob_mes = df_filtrado.groupby("mes")["valor_fob"].sum().reset_index()
fig1 = px.bar(fob_mes, x="mes", y="valor_fob", labels={"mes": "Mês", "valor_fob": "Valor FOB"}, title="Valor FOB por Mês")
st.plotly_chart(fig1, use_container_width=True)

top_ncm = df_filtrado.groupby(["ncm", "descricao_ncm"])["valor_fob"].sum().reset_index()
top_ncm = top_ncm.sort_values(by="valor_fob", ascending=False).head(10)
fig2 = px.bar(top_ncm, x="valor_fob", y="descricao_ncm", orientation="h", title="Top 10 Produtos (por NCM)",
              labels={"valor_fob": "Valor FOB", "descricao_ncm": "Descrição NCM"})
st.plotly_chart(fig2, use_container_width=True)

fob_pais = df_filtrado.groupby("pais")["valor_fob"].sum().reset_index().sort_values(by="valor_fob", ascending=False).head(15)
fig3 = px.bar(fob_pais, x="valor_fob", y="pais", orientation="h", title="Top 15 Países",
              labels={"valor_fob": "Valor FOB", "pais": "País"})
st.plotly_chart(fig3, use_container_width=True)

fob_uf = df_filtrado.groupby("uf")["valor_fob"].sum().reset_index().sort_values(by="valor_fob", ascending=False)
fig4 = px.bar(fob_uf, x="uf", y="valor_fob", title="Movimentação por UF", labels={"valor_fob": "Valor FOB", "uf": "UF"})
st.plotly_chart(fig4, use_container_width=True)

st.markdown("## 📄 Registros Filtrados")
st.dataframe(df_filtrado, use_container_width=True)
