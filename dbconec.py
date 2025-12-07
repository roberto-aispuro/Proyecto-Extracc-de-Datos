import pyodbc
import streamlit as st

@st.cache_resource(ttl=3600)
def get_db_connection():
    try:
        return pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=SBTIJRAISPURO\\VE_SERVER;'
            'DATABASE=MIGRACION_INEGI;'
            'Trusted_Connection=yes;'
        )
    except Exception as e:
        st.error(f"No se pudo conectar a la base de datos: {e}")
        st.stop()