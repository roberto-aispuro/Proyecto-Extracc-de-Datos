import pyodbc
import pandas as pd
import os


def conectar():
    try:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=SBTIJRAISPURO\\VE_SERVER;'
            'DATABASE=MIGRACION_INEGI;'
            'Trusted_Connection=yes;'
        )
        print("Conexión exitosa")
        return conn
    except Exception as e:
        print("Error:", e)
        return None


def crear_tablas():
    conn = conectar()
    if not conn:
        return
    cursor = conn.cursor()

    # Tabla para migracion_mexico_2000_2010_2020.csv
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='migracion_mexico_2000_2010_2020' AND xtype='U')
        CREATE TABLE migracion_mexico_2000_2010_2020 (
            Entidad_federativa VARCHAR(100),
            Inmigrante_2000 INT,
            Emigrante_2000 INT,
            Saldo_neto_2000 INT,
            Inmigrante_2010 INT,
            Emigrante_2010 INT,
            Saldo_neto_2010 INT,
            Inmigrante_2020 INT,
            Emigrante_2020 INT,
            Saldo_neto_2020 INT,
        )
    ''')

    # Tabla para migracion_interna_por_entidad_2020.csv
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='migracion_interna_por_entidad_2020' AND xtype='U')
        CREATE TABLE migracion_interna_por_entidad_2020 (
            Entidad_federativa VARCHAR(100),
            Misma_entidad_5_años_antes_porcentaje FLOAT,
            Otra_entidad_5_años_antes_porcentaje FLOAT,
            Otro_país_5_años_antes_porcentaje FLOAT,
        )
    ''')

    # Tabla para emigracion_internacional_a_eeuu_por_entidad_2023.csv
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='emigracion_internacional_a_eeuu_por_entidad_2023' AND xtype='U')
        CREATE TABLE emigracion_internacional_a_eeuu_por_entidad_2023 (
            Entidad_federativa VARCHAR(100),
            Porcentaje_emigrante_a_EEUU_2018_2023 FLOAT
        )
    ''')

    # Tabla para causas_migracion_2020.csv (nueva)
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='causas_migracion_2020' AND xtype='U')
        CREATE TABLE causas_migracion_2020 (
            Causa_de_migracion VARCHAR(100),
            Porcentaje_2020 FLOAT
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()
    print("Todas las tablas estan creadas")


def insertar_datos():
    conn = conectar()
    if not conn:
        return
    cursor = conn.cursor()

    # Insertar migracion_mexico_2000_2010_2020.csv
    ruta1 = 'dataset/migracion_mexico_2000_2010_2020.csv'
    if os.path.exists(ruta1):
        df = pd.read_csv(ruta1)
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO migracion_mexico_2000_2010_2020 
                (Entidad_federativa, Inmigrante_2000, Emigrante_2000, Saldo_neto_2000,
                 Inmigrante_2010, Emigrante_2010, Saldo_neto_2010,
                 Inmigrante_2020, Emigrante_2020, Saldo_neto_2020)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', row['Entidad federativa'],
                           int(row['Inmigrante_2000']) if pd.notna(row['Inmigrante_2000']) else None,
                           int(row['Emigrante_2000']) if pd.notna(row['Emigrante_2000']) else None,
                           int(row['Saldo_neto_2000']) if pd.notna(row['Saldo_neto_2000']) else None,
                           int(row['Inmigrante_2010']) if pd.notna(row['Inmigrante_2010']) else None,
                           int(row['Emigrante_2010']) if pd.notna(row['Emigrante_2010']) else None,
                           int(row['Saldo_neto_2010']) if pd.notna(row['Saldo_neto_2010']) else None,
                           int(row['Inmigrante_2020']) if pd.notna(row['Inmigrante_2020']) else None,
                           int(row['Emigrante_2020']) if pd.notna(row['Emigrante_2020']) else None,
                           int(row['Saldo_neto_2020']) if pd.notna(row['Saldo_neto_2020']) else None)
        print(f"Datos de {ruta1} insertados")
    else:
        print(f"Archivo {ruta1} no encontrado. Asegúrate de tenerlo en el directorio actual.")

    # Insertar migracion_interna_por_entidad_2020.csv
    ruta2 = 'dataset/migracion_interna_por_entidad_2020.csv'
    if os.path.exists(ruta2):
        df = pd.read_csv(ruta2)
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO migracion_interna_por_entidad_2020 
                (Entidad_federativa, Misma_entidad_5_años_antes_porcentaje, 
                 Otra_entidad_5_años_antes_porcentaje, Otro_país_5_años_antes_porcentaje)
                VALUES (?, ?, ?, ?)
            ''', row['Entidad_federativa'],
                           float(row['Misma_entidad_5_años_antes_%']) if pd.notna(
                               row['Misma_entidad_5_años_antes_%']) else None,
                           float(row['Otra_entidad_5_años_antes_%']) if pd.notna(
                               row['Otra_entidad_5_años_antes_%']) else None,
                           float(row['Otro_país_5_años_antes_%']) if pd.notna(
                               row['Otro_país_5_años_antes_%']) else None)
        print(f"Datos de {ruta2} insertados")
    else:
        print(f"Archivo {ruta2} no encontrado. Asegúrate de tenerlo en el directorio actual.")

    # Insertar emigracion_internacional_a_eeuu_por_entidad_2023.csv
    ruta3 = 'dataset/emigracion_internacional_a_eeuu_por_entidad_2023.csv'
    if os.path.exists(ruta3):
        df = pd.read_csv(ruta3)
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO emigracion_internacional_a_eeuu_por_entidad_2023 
                (Entidad_federativa, Porcentaje_emigrante_a_EEUU_2018_2023)
                VALUES (?, ?)
            ''', row['Entidad_federativa'],
                           float(row['Porcentaje_emigrante_a_EEUU_2018_2023']) if pd.notna(
                               row['Porcentaje_emigrante_a_EEUU_2018_2023']) else None)
        print(f"Datos de {ruta3} insertados")
    else:
        print(f"Archivo {ruta3} no encontrado. Asegúrate de tenerlo en el directorio actual.")

    # Insertar causas_migracion_2020.csv (nueva)
    ruta4 = 'dataset/causas_migracion_2020.csv'
    if os.path.exists(ruta4):
        df = pd.read_csv(ruta4)
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO causas_migracion_2020 
                (Causa_de_migracion, Porcentaje_2020)
                VALUES (?, ?)
            ''', row['Causa_de_migracion'],
                           float(row['Porcentaje_2020']) if pd.notna(row['Porcentaje_2020']) else None)
        print(f"Datos de {ruta4} insertados")
    else:
        print(f"Archivo {ruta4} no encontrado.")

    conn.commit()
    cursor.close()
    conn.close()
    print("Inserciones completas")


