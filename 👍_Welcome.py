
import streamlit as st

st.set_page_config(page_title="Migración México", layout="wide")

st.title("Migración en México 2000-2020")
st.markdown("### Dashboard Interactivo con datos del INEGI")

st.image("pages/inegi.svg", width=200)

st.markdown("""
**Explora los datos de migración interna e internacional**

- **Tendencias** → Evolución histórica
- **Comparaciones** → Entre estados
- **KPIs y Causas** → Motivos y estadísticas clave
""")

