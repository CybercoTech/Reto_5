# module_txt.py

import os
import re
import string
from collections import Counter

import matplotlib.pyplot as plt

from utilities import (limpiar_pantalla, pausar, animacion_carga, VERDE, ROJO, AZUL, AMARILLO, NEGRITA, RESET)


DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_OUTPUTS = os.path.join(DIRECTORIO_BASE, "Outputs")

if not os.path.exists(RUTA_OUTPUTS):
    os.makedirs(RUTA_OUTPUTS)

plt.style.use('dark_background')

CONECTORES = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", 
    "al", "a", "en", "y", "o", "que", "con", "por", "para", "es", "se",
    "su", "sus", "lo", "como", "más", "pero", "si", "no", "este", "esta"
}

def cargar_texto(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        print(f"{ROJO}--- Error: El archivo '{ruta_archivo}' no existe.{RESET}")
        return None
        
    try:
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
            if not lineas:
                print(f"{ROJO}--- El archivo está vacío.{RESET}")
                return None
            return lineas
    except Exception as e:
        print(f"{ROJO}--- Error al leer el archivo: {e}{RESET}")
        return None

def resumen_estadistico(lineas):

    limpiar_pantalla()
    print(f"{NEGRITA}{AZUL}--- RESUMEN ESTADÍSTICO DEL TEXTO {RESET}")
    
    animacion_carga("Analizando texto")
    
    total_lineas = len(lineas)
    texto_completo = "".join(lineas)
    
    total_caracteres_con_espacios = len(texto_completo)
    total_caracteres_sin_espacios = len(texto_completo.replace(" ", "").replace("\n", ""))
    
    texto_limpio = texto_completo.lower()
    for signo in string.punctuation:
        texto_limpio = texto_limpio.replace(signo, "")
        
    palabras = texto_limpio.split()
    total_palabras = len(palabras)

    palabras_filtradas = [p for p in palabras if p not in CONECTORES]
    

    contador = Counter(palabras_filtradas)
    top_5 = contador.most_common(5)
    
    print(f"\n--- {NEGRITA}Estadísticas Generales:{RESET}")
    print(f"  -- Total de líneas           : {total_lineas}")
    print(f"  -- Total de palabras         : {total_palabras}")
    print(f"  -- Caracteres (con espacios) : {total_caracteres_con_espacios}")
    print(f"  -- Caracteres (sin espacios) : {total_caracteres_sin_espacios}")
    
    print(f"\n {NEGRITA}--- Top 5 Palabras más repetidas (sin conectores):{RESET}")
    for i, (palabra, frecuencia) in enumerate(top_5, 1):
        print(f"  {i}. {VERDE}{palabra}{RESET} -> Aparece {frecuencia} veces")
        
    pausar()
    return contador 

def extraer_patrones(lineas):

    limpiar_pantalla()
    print(f"{NEGRITA}{AZUL}--- EXTRACCIÓN DE PATRONES (BÚSQUEDA) {RESET}")
    print("--- Ideal para buscar errores en logs (ej. 'ERROR', '404', 'WARNING').")
    
    patron = input(f"\n{VERDE}--- Ingresa la palabra o patrón a buscar: {RESET}").strip()
    
    if not patron:
        return
        
    animacion_carga(f"Buscando '{patron}'")
    
    texto_completo = "".join(lineas)
  

    coincidencias = re.findall(patron, texto_completo, re.IGNORECASE)
    total = len(coincidencias)
    
    if total > 0:
        print(f"\n--- Se encontraron {NEGRITA}{total}{RESET} coincidencias para '{patron}'.")

        print(f"\n{AMARILLO}--- Ejemplos de líneas donde aparece:{RESET}")
        ejemplos_mostrados = 0
        
        for linea in lineas:
            if re.search(patron, linea, re.IGNORECASE):
                print(f"  > {linea.strip()[:100]}...") 
                ejemplos_mostrados += 1
                
                if ejemplos_mostrados >= 3: 
                    break
    else:
        print(f"\n{AMARILLO}--- No se encontró el patrón '{patron}' en el archivo.{RESET}")
        
    pausar()

def grafico_barras_horizontal(lineas):

    limpiar_pantalla()
    print(f"{NEGRITA}{AZUL}--- GRÁFICO 1: TOP 10 PALABRAS CLAVE {RESET}")
    
    animacion_carga("Generando gráfico de frecuencias")
    
    texto_completo = "".join(lineas).lower()
    for signo in string.punctuation:
        texto_completo = texto_completo.replace(signo, "")
        
    palabras = [p for p in texto_completo.split() if p not in CONECTORES]
    contador = Counter(palabras)
    top_10 = contador.most_common(10)
    

    palabras_grafico = [item[0] for item in reversed(top_10)]
    frecuencias = [item[1] for item in reversed(top_10)]
    
    plt.figure(figsize=(10, 6))
    plt.barh(palabras_grafico, frecuencias, color='#00bcd4', edgecolor='white')
    plt.title('Top 10 Palabras más Frecuentes', fontsize=15, pad=15)
    plt.xlabel('Frecuencia (Apariciones)', fontsize=12)
    plt.ylabel('Palabras', fontsize=12)
    

    for i, v in enumerate(frecuencias):
        plt.text(v + 0.5, i, str(v), color='white', va='center', fontweight='bold')
        
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    nombre_archivo = os.path.join(RUTA_OUTPUTS, "grafico_top10_palabras.png")
    plt.savefig(nombre_archivo)
    plt.close()
    
    print(f"\n{VERDE}--- Gráfico guardado en '{nombre_archivo}'{RESET}")
    pausar()

def grafico_histograma_longitudes(lineas):

    limpiar_pantalla()
    print(f"{NEGRITA}{AZUL}--- GRÁFICO 2: DISTRIBUCIÓN DE LONGITUD DE LÍNEAS {RESET}")
    
    animacion_carga("Calculando longitudes")
    
    longitudes = [len(linea.strip()) for linea in lineas]
    
    plt.figure(figsize=(10, 6))
    plt.hist(longitudes, bins=15, color='#8e44ad', edgecolor='white', alpha=0.8)
    
    plt.title('Distribución de Longitud de las Líneas', fontsize=15, pad=15)
    plt.xlabel('Cantidad de Caracteres por Línea', fontsize=12)
    plt.ylabel('Cantidad de Líneas', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    nombre_archivo = os.path.join(RUTA_OUTPUTS, "grafico_histograma_longitudes.png")
    plt.savefig(nombre_archivo)
    plt.close()
    
    print(f"\n{VERDE}--- Gráfico guardado en '{nombre_archivo}'{RESET}")
    pausar()

def grafico_palabras_por_linea(lineas):

    limpiar_pantalla()
    print(f"{NEGRITA}{AZUL}--- GRÁFICO 8: DENSIDAD DE PALABRAS POR LÍNEA {RESET}")
    print("--- Analiza las primeras 50 líneas para ver cómo fluctúa la longitud del texto.")
    
    lineas_muestra = lineas[:50]
    cantidad_palabras = []
    
    for linea in lineas_muestra:
        palabras = linea.strip().split()
        cantidad_palabras.append(len(palabras))
        
    animacion_carga("Generando gráfico de densidad")
    
    plt.figure(figsize=(12, 5))
    plt.plot(range(1, len(cantidad_palabras) + 1), cantidad_palabras, marker='o', color='#e74c3c', linewidth=2)
    
    plt.title('Cantidad de Palabras por Línea (Primeras 50 líneas)', fontsize=14)
    plt.xlabel('Número de Línea')
    plt.ylabel('Cantidad de Palabras')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    nombre_archivo = os.path.join(RUTA_OUTPUTS, "grafico_palabras_por_linea.png")
    plt.savefig(nombre_archivo)
    plt.close()
    
    print(f"\n{VERDE}--- Gráfico guardado exitosamente en '{nombre_archivo}'{RESET}")
    pausar()

def menu_analisis_txt():
   
    limpiar_pantalla()
    print(f"{NEGRITA}{AZUL}--- MÓDULO DE PROCESAMIENTO DE TEXTOS (.TXT) {RESET}")
    
    ruta_defecto = os.path.join(DIRECTORIO_BASE, "Data", "log.txt")
    ruta = input(f"{VERDE}--- Ingresa la ruta del archivo .txt (Enter para usar '{ruta_defecto}'): {RESET}").strip()
    if not ruta:
        ruta = ruta_defecto 
        
    animacion_carga("Cargando archivo de texto")
    lineas = cargar_texto(ruta)
    
    if not lineas:
        pausar()
        return
        
    while True:
        limpiar_pantalla()
        print(f"{NEGRITA}--- ANÁLISIS DE TEXTO: {os.path.basename(ruta)}{RESET}")
        print("--- 1. Resumen Estadístico y Top 5 Palabras")
        print("--- 2. Extracción de Patrones (Buscar errores/palabras)")
        print("--- 3. Generar Gráfico: Top 10 Palabras (Barras Horizontales)")
        print("--- 4. Generar Gráfico: Distribución de Longitud de Líneas (Histograma)")
        print("--- 5. Generar Gráfico: Densidad de Palabras (Líneas 1-50)")
        print(f"{ROJO}--- 6. Volver al menú principal{RESET}")
        
        opcion = input(f"\n{AZUL}--- Elige una opción (1-6): {RESET}").strip()
        
        if opcion == '1':
            resumen_estadistico(lineas)
            
        elif opcion == '2':
            extraer_patrones(lineas)
            
        elif opcion == '3':
            grafico_barras_horizontal(lineas)
            
        elif opcion == '4':
            grafico_histograma_longitudes(lineas)
            
        elif opcion == '5':
            grafico_palabras_por_linea(lineas)
            
        elif opcion == '6':
            break
            
        else:
            print(f"{ROJO}--- Opción no válida.{RESET}")
            pausar()