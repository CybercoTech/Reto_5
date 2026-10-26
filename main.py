# main.py

import sys
import os

from utilities import ( limpiar_pantalla, pausar, mostrar_banner, animacion_carga, formatear_tamano, validar_ruta, VERDE, ROJO, AZUL, AMARILLO, NEGRITA, RESET)

from module_csv import menu_analisis_csv
from module_txt import menu_analisis_txt

def explorar_directorio():
    
    limpiar_pantalla()
    print(f"{NEGRITA}{AZUL}  ------ EXPLORADOR DE DIRECTORIOS {RESET}")
    print("--- Por defecto, puedes presionar Enter para usar la carpeta actual (./Data).")
    
    ruta_usuario = input(f"\n{VERDE}--- Ingresa la ruta a explorar: {RESET}").strip()
    

    if not ruta_usuario:
        ruta_usuario = "./Data"
        

    if not validar_ruta(ruta_usuario):
        print(f"\n{ROJO} --- Error: La ruta '{ruta_usuario}' no existe o no es válida.{RESET}")
        pausar()
        return 
    
    animacion_carga(f"Buscando archivos en '{ruta_usuario}'")
    
    try:
       
        elementos = os.listdir(ruta_usuario)
        
        archivos_txt = []
        archivos_csv = []
        
       
        for elemento in elementos:
            ruta_completa = os.path.join(ruta_usuario, elemento)
           
            if os.path.isfile(ruta_completa):
                if elemento.lower().endswith('.txt'):
                    archivos_txt.append((elemento, ruta_completa))
                elif elemento.lower().endswith('.csv'):
                    archivos_csv.append((elemento, ruta_completa))
        
        print(f"\n{NEGRITA}--- Archivos .TXT encontrados:{RESET}")
        if not archivos_txt:
            print(f"  {AMARILLO}--- No se encontraron archivos .txt.{RESET}")
        else:
            for nombre, ruta in archivos_txt:
            
                peso_bytes = os.path.getsize(ruta)
                peso_legible = formatear_tamano(peso_bytes)
                print(f"   {VERDE}{nombre}{RESET} ({peso_legible})")
                
        print(f"\n{NEGRITA}--- Archivos .CSV encontrados:{RESET}")
        if not archivos_csv:
            print(f"  {AMARILLO}--- No se encontraron archivos .csv.{RESET}")
        else:
            for nombre, ruta in archivos_csv:
                peso_bytes = os.path.getsize(ruta)
                peso_legible = formatear_tamano(peso_bytes)
                print(f"{VERDE}{nombre}{RESET} ({peso_legible})")
                
        print(f"\n{AMARILLO}--- Total de archivos analizables: {len(archivos_txt) + len(archivos_csv)}{RESET}")
        
    except PermissionError:
        print(f"\n{ROJO}--- Error: No tienes permisos para acceder a esta carpeta.{RESET}")
    except Exception as e:
        print(f"\n{ROJO}--- Ocurrió un error inesperado: {e}{RESET}")
        
    pausar()

def main():
    while True:
        limpiar_pantalla()
        mostrar_banner()
        
        print(f"{NEGRITA}------ MENÚ PRINCIPAL{RESET}")
        print(f"--- 1. {VERDE}Explorar directorio{RESET} (Listar archivos disponibles)")
        print(f"--- 2. {VERDE}Procesar Bitácoras / Textos Reales (.txt){RESET}")
        print(f"--- 3. {VERDE}Analizar Dataset de Datos Abiertos (.csv){RESET}")
        print(f"--- 4. {ROJO}Salir del programa{RESET}")                
        
        opcion = input(f"\n{AZUL}--- Elige una opción (1-4): {RESET}").strip()
        
        if opcion == '1':
            explorar_directorio()
        
        elif opcion == '2':
            menu_analisis_txt()

        elif opcion == '3':
            menu_analisis_csv() 
        
        elif opcion == '4':
            limpiar_pantalla()
            print(f"{VERDE}--- Saliendo del programa.{RESET}")
            sys.exit()
        
        else:
            print(f"\n{ROJO}--- Opción no válida. Por favor, ingresa un número del 1 al 4.{RESET}")
            pausar()
if __name__ == "__main__":
    main()