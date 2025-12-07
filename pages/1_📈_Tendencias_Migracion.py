import streamlit as st
import pandas as pd
import plotly.express as px
import dbconec as cxn

@st.cache_data(ttl=3600)
def load_data():
    conn = cxn.get_db_connection()
    df = pd.read_sql("SELECT * FROM migracion_mexico_2000_2010_2020", conn)
    return df

st.title("Tendencias de Migración en México (2000-2020)")

df = load_data()

# Filtros
col1, col2 = st.columns(2)
with col1:
    entidad = st.selectbox("Selecciona una entidad", ["Todas"] + sorted(df['Entidad_federativa'].unique()))
with col2:
    tipo = st.radio("Ver:", ["Inmigrantes", "Emigrantes", "Saldo Neto"], horizontal=True)

# Preparar datos largos
if tipo == "Inmigrantes":
    vars = ['Inmigrante_2000', 'Inmigrante_2010', 'Inmigrante_2020']
    titulo = "Evolución de Inmigrantes"
elif tipo == "Emigrantes":
    vars = ['Emigrante_2000', 'Emigrante_2010', 'Emigrante_2020']
    titulo = "Evolución de Emigrantes"
else:
    vars = ['Saldo_neto_2000', 'Saldo_neto_2010', 'Saldo_neto_2020']
    titulo = "Evolución del Saldo Neto Migratorio"

df_long = df.melt(id_vars='Entidad_federativa', value_vars=vars,
                  var_name='Año', value_name='Personas')
df_long['Año'] = df_long['Año'].str.extract('(\d{4})').astype(int)
df_long['Personas'] = pd.to_numeric(df_long['Personas'], errors='coerce')

if entidad != "Todas":
    df_long = df_long[df_long['Entidad_federativa'] == entidad]

fig = px.line(df_long, x="Año", y="Personas", color="Entidad_federativa",
              title=titulo, markers=True, template="plotly_white")
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

st.info(f"Total {tipo.lower()} en 2020: {df[vars[-1]].sum():,} personas")