import streamlit as st
import pandas as pd
import plotly.express as px
import dbconec as cxn
@st.cache_data(ttl=3600)
def load_all():
    conn = cxn.get_db_connection()
    df1 = pd.read_sql("SELECT * FROM migracion_mexico_2000_2010_2020", conn)
    df2 = pd.read_sql("SELECT * FROM emigracion_internacional_a_eeuu_por_entidad_2023", conn)

    return df1, df2

st.title("Comparación entre Estados")

df_general, df_eeuu = load_all()

entidades = st.multiselect(
    "Selecciona hasta 10 estados para comparar",
    options=sorted(df_general['Entidad_federativa'].unique()),
    default=["Ciudad de México", "Jalisco", "Nuevo León", "Michoacán de Ocampo", "Guerrero", "Zacatecas"]
)

if not entidades:
    st.warning("Selecciona al menos una entidad")
else:
    df_comp = df_general[df_general['Entidad_federativa'].isin(entidades)].copy()
    df_eeuu_comp = df_eeuu[df_eeuu['Entidad_federativa'].isin(entidades)]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Saldo Neto Migratorio 2020")
        df_comp['Saldo_neto_2020'] = pd.to_numeric(df_comp['Saldo_neto_2020'], errors='coerce')
        fig1 = px.bar(df_comp.sort_values("Saldo_neto_2020"),
                      x="Entidad_federativa", y="Saldo_neto_2020",
                      color="Saldo_neto_2020", color_continuous_scale="RdYlGn",
                      text_auto=True)
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Porcentaje que emigró a EUA (2018-2023)")
        fig2 = px.bar(df_eeuu_comp.sort_values("Porcentaje_emigrante_a_EEUU_2018_2023", ascending=True),
                      y="Entidad_federativa", x="Porcentaje_emigrante_a_EEUU_2018_2023",
                      orientation='h', color="Porcentaje_emigrante_a_EEUU_2018_2023",
                      color_continuous_scale="Reds", text_auto=".1f")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Inmigrantes recibidos en 2020")
    fig3 = px.treemap(df_comp, path=['Entidad_federativa'], values='Inmigrante_2020',
                      color='Inmigrante_2020', color_continuous_scale="Blues")
    st.plotly_chart(fig3, use_container_width=True)