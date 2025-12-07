import time
import etapa_uno as e1
import etapa_dos as e2
import etapa_tres as e3

def menu():
    while True:
        print("\n" + "="*70)
        print("          MENU DE PROYECTO DE MIGRACIÓN MÉXICO - INEGI 2020")
        print("="*70)
        print("1. Extracción de datos del INEGI (CSV)")
        print("2. Carga y creación de tablas en SQL")
        print("3. Abrir Dashboard Interactivo (Streamlit)")
        print("4. Salir")
        print("-"*70)

        opc = input("Elige una opción (1-4): ").strip()

        if opc == "1":
            print("\nIniciando extracción de datos del INEGI...")
            e1.tabla1()
            e1.tabla2()
            e1.tabla3()
            e1.tabla4()
            print("Extracción completada. Archivos en carpeta 'dataset/'")

        elif opc == "2":
            print("\nCreando tablas e insertando datos en SQL Server...")
            e2.crear_tablas()
            e2.insertar_datos()
            print("Datos cargados correctamente en la base de datos.")

        elif opc == "3":
            print("\nAbriendo Dashboard Interactivo...")
            e3.main()

        elif opc == "4":
            print("\n¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")
            time.sleep(2)

if __name__ == "__main__":
    menu()