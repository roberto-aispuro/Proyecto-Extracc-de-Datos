import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def service():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--window-size=1200,1000")
    driver = webdriver.Chrome(service=service, options=options)

    return driver

def tabla1():
    driver=service()

    url = "https://www.inegi.org.mx/app/tabulados/interactivos/?pxq=Migracion_Migracion_01_426da5e7-766a-42a9-baef-5768cde4fca9&idrt=130&opc=t"
    driver.get(url)
    time.sleep(10)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    tabla = soup.find("table", class_="zpop8FeV7OkeeMKGX-soi")
    filas = tabla.find("tbody").find_all("tr")

    datos = []
    entidad_actual = ""

    for fila in filas:
        celdas = fila.find_all("td")

        # Si la primera celda tiene clase de entidad o tiene texto  es una nueva entidad
        if celdas and ("_2abKlxeJ1e1K8zCGSsxn_8" in celdas[0].get("class", []) or celdas[0].get_text(strip=True)):
            entidad_actual = celdas[0].get_text(strip=True)
            valores = celdas[1:]  # los 9 valores están desde la posición 1
        else:
            # Es una fila continuada (sin celda de entidad)  usar la entidad anterior
            valores = celdas  # aquí vienen los 9 valores directamente

        # Extraer los 9 valores numéricos
        valores_texto = [td.get_text(strip=True).replace(",", "") for td in valores[:9]]

        if len(valores_texto) == 9:
            registro = {
                "Entidad federativa": entidad_actual,
                "Inmigrante_2000": valores_texto[0],
                "Emigrante_2000": valores_texto[1],
                "Saldo_neto_2000": valores_texto[2],
                "Inmigrante_2010": valores_texto[3],
                "Emigrante_2010": valores_texto[4],
                "Saldo_neto_2010": valores_texto[5],
                "Inmigrante_2020": valores_texto[6],
                "Emigrante_2020": valores_texto[7],
                "Saldo_neto_2020": valores_texto[8],
            }
            datos.append(registro)

    # Crear carpeta y guardar
    os.makedirs("dataset", exist_ok=True)
    df = pd.DataFrame(datos)
    df.to_csv("dataset/migracion_mexico_2000_2010_2020.csv", index=False, encoding="utf-8-sig")
    print("Archivo guardado en: dataset/migracion_mexico_2000_2010_2020.csv")
    return df

def tabla2():
    driver=service()

    print("Abriendo página del INEGI...")
    driver.get("https://www.inegi.org.mx/temas/migracion/")
    time.sleep(12)  # Espera carga inicial

    try:
        # PASO CLAVE: Hacer clic en el botón "Tabla"
        print("Haciendo clic en el botón 'Tabla'...")
        btn_tabla = driver.find_element(By.ID, "btn_tablagraf_gral0")
        btn_tabla.click()
        time.sleep(4)  # Espera a que aparezca la tabla

        # Verificar que la tabla ya está visible
        print("Esperando a que aparezca la tabla...")
        tabla = driver.find_element(By.ID, "tableStatcontGraficagraf_gral0")
        time.sleep(2)

        # Extraer datos con BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        tabla_html = soup.find("table", id="tableStatcontGraficagraf_gral0")

        datos = []
        for fila in tabla_html.find("tbody").find_all("tr"):
            th = fila.find("th", class_="TdInicio")
            td = fila.find("td", class_="Td")
            if th and td:
                datos.append({
                    "Causa_de_migracion": th.get_text(strip=True),
                    "Porcentaje_2020": td.get_text(strip=True).strip()
                })

        driver.quit()

        # Guardar CSV
        os.makedirs("dataset", exist_ok=True)
        df = pd.DataFrame(datos)
        ruta = "dataset/causas_migracion_2020.csv"
        df.to_csv(ruta, index=False, encoding="utf-8-sig")

        print(f"\nÉXITO TOTAL!")
        print(f"Se extrajeron {len(df)} causas de migración (2020)")
        print("Archivo guardado en:", ruta)
        print("\nDatos extraídos:")
        print(df.to_string(index=False))

        return df

    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return None

def tabla3():
    driver=service()

    print("Abriendo página del INEGI - Migración...")
    driver.get("https://www.inegi.org.mx/temas/migracion/")
    time.sleep(12)  # Carga completa

    try:
        # 1. Hacer clic en el botón "Tabla" de la sección correcta
        print("Haciendo clic en el botón de la tabla de migración interna...")
        btn_tabla = driver.find_element(By.ID, "btn_tablacont00")
        btn_tabla.click()
        time.sleep(5)  # Espera a que cargue la tabla

        # 2. Verificar que la tabla esté visible
        print("Buscando la tabla de migración interna...")
        tabla = driver.find_element(By.ID, "tableStatcontGraficacont00")
        time.sleep(3)

        # 3. Extraer con BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        tabla_html = soup.find("table", id="tableStatcontGraficacont00")

        datos = []
        filas = tabla_html.find("tbody").find_all("tr")

        for fila in filas:
            celdas = fila.find_all("td")
            if len(celdas) == 4:
                entidad = celdas[0].get_text(strip=True)
                misma_entidad = celdas[1].get_text(strip=True)
                otra_entidad = celdas[2].get_text(strip=True)
                otro_pais = celdas[3].get_text(strip=True)

                datos.append({
                    "Entidad_federativa": entidad,
                    "Misma_entidad_5_años_antes_%": misma_entidad,
                    "Otra_entidad_5_años_antes_%": otra_entidad,
                    "Otro_país_5_años_antes_%": otro_pais
                })

        driver.quit()

        # 4. Guardar en CSV
        os.makedirs("dataset", exist_ok=True)
        df = pd.DataFrame(datos)
        ruta = "dataset/migracion_interna_por_entidad_2020.csv"
        df.to_csv(ruta, index=False, encoding="utf-8-sig")

        print(f"\nÉXITO TOTAL!")
        print(f"Se extrajeron {len(df)} entidades federativas")
        print("Archivo guardado en:", ruta)
        print("\nPrimeras 10 filas:")
        print(df.head(10).to_string(index=False))

        return df

    except Exception as e:
        print(f"Error: {e}")
        driver.save_screenshot("dataset/error_migracion_interna.png")  # Para debug
        driver.quit()
        return None

def tabla4():
    driver=service()

    print("Abriendo página del INEGI - Migración...")
    driver.get("https://www.inegi.org.mx/temas/migracion/")
    time.sleep(12)  # Espera carga completa

    try:
        # 1. Hacer clic en el botón "Tabla" de la sección correcta
        print("Haciendo clic en 'Tabla' para ver emigración a EUA...")
        boton_tabla = driver.find_element(By.ID, "btn_tablacont02")
        driver.execute_script("arguments[0].click();", boton_tabla)
        time.sleep(5)

        # 2. Esperar a que aparezca la tabla
        print("Esperando a que cargue la tabla de emigración a Estados Unidos...")
        tabla = driver.find_element(By.ID, "tableStatcontGraficacont02")
        time.sleep(4)

        # 3. Extraer datos con BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        tabla_html = soup.find("table", id="tableStatcontGraficacont02")

        datos = []
        filas = tabla_html.find("tbody").find_all("tr")

        for fila in filas:
            celdas = fila.find_all("td")
            if len(celdas) == 2:
                entidad = celdas[0].get_text(strip=True)
                porcentaje = celdas[1].get_text(strip=True)

                datos.append({
                    "Entidad_federativa": entidad,
                    "Porcentaje_emigrante_a_EEUU_2018_2023": porcentaje
                })

        driver.quit()

        # 4. Guardar en CSV
        os.makedirs("dataset", exist_ok=True)
        df = pd.DataFrame(datos)
        ruta = "dataset/emigracion_internacional_a_eeuu_por_entidad_2023.csv"
        df.to_csv(ruta, index=False, encoding="utf-8-sig")

        print(f"\nÉXITO TOTAL!")
        print(f"Se extrajeron {len(df)} entidades")
        print("Datos extraídos:")
        print(df.head(15).to_string(index=False))
        print(f"\nArchivo guardado en: {ruta}")

        return df

    except Exception as e:
        print(f"Error: {e}")
        driver.save_screenshot("dataset/error_emigracion_eeuu.png")
        driver.quit()
        return None

