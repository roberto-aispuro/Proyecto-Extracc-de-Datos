import streamlit as st
import pandas as pd
import plotly.express as px
import dbconec as cxn

@st.cache_data(ttl=3600)
def load_kpis():
    conn = cxn.get_db_connection()
    df_main = pd.read_sql("SELECT * FROM migracion_mexico_2000_2010_2020", conn)
    df_causas = pd.read_sql("SELECT * FROM causas_migracion_2020", conn)
    df_eeuu = pd.read_sql("SELECT * FROM emigracion_internacional_a_eeuu_por_entidad_2023", conn)
    # NO cerrar conn aquí
    return df_main, df_causas, df_eeuu

st.title("KPIs y Causas de Migración")

df, causas, eeuu = load_kpis()

# KPIs
inm_2020 = int(df['Inmigrante_2020'].sum())
emi_2020 = int(df['Emigrante_2020'].sum())
saldo = inm_2020 - emi_2020
prom_eeuu = eeuu['Porcentaje_emigrante_a_EEUU_2018_2023'].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Inmigrantes 2020", f"{inm_2020:,}")
c2.metric("Emigrantes 2020", f"{emi_2020:,}")
c3.metric("Saldo Neto 2020", f"{saldo:+,}")
c4.metric("Promedio emigró a EUA", f"{prom_eeuu:.1f}%")

# Gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader("Principales Causas de Migración 2020")
    causas['Porcentaje_2020'] = pd.to_numeric(causas['Porcentaje_2020'], errors='coerce')
    fig_pie = px.pie(causas, values='Porcentaje_2020', names='Causa_de_migracion',
                     color_discrete_sequence=px.colors.sequential.Plasma)
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("Top 10 Estados que más emigran a EUA")
    top10 = eeuu.nlargest(10, 'Porcentaje_emigrante_a_EEUU_2018_2023')
    fig_bar = px.bar(top10, x='Porcentaje_emigrante_a_EEUU_2018_2023', y='Entidad_federativa',
                     orientation='h', text_auto='.1f', color='Porcentaje_emigrante_a_EEUU_2018_2023',
                     color_continuous_scale="Reds")
    fig_bar.update_layout(height=500)
    st.plotly_chart(fig_bar, use_container_width=True)

st.success("Datos actualizados desde INEGI - Censo 2020 y ENADID")