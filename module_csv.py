# module_csv.py

import csv
import os
import matplotlib.pyplot as plt

from utilities import (limpiar_pantalla, pausar, animacion_carga, VERDE, ROJO, AZUL, AMARILLO, NEGRITA, RESET)

DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_OUTPUTS = os.path.join(DIRECTORIO_BASE, "Outputs")

if not os.path.exists(RUTA_OUTPUTS):
    os.makedirs(RUTA_OUTPUTS)

plt.style.use('dark_background')

def cargar_datos_csv(ruta_archivo):

    if not os.path.exists(ruta_archivo):
        print(f"{ROJO}--- Error: El archivo '{ruta_archivo}' no existe.{RESET}")
        return None, None
        
    try:
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:

            lector = csv.DictReader(archivo)
            cabeceras = lector.fieldnames
            datos = list(lector) 
            
            if not datos:
                print(f"{ROJO}--- El archivo CSV está vacío.{RESET}")
                return None, None
                
            return datos, cabeceras
    except Exception as e:
        print(f"{ROJO}--- Error al leer el archivo: {e}{RESET}")
        return None, None

def mostrar_vista_previa(datos, cabeceras):

    limpiar_pantalla()
    print(f"{NEGRITA}{AZUL}------ VISTA PREVIA DEL DATASET {RESET}")
    
    print(f"{AMARILLO}{' | '.join(str(c) for c in cabeceras)}{RESET}")
    print("------")
    
    for fila in datos[:10]:
        valores = [str(fila[c]) for c in cabeceras]
        print(" | ".join(valores))
        
    print(f"\n{AMARILLO}--- Cortando para no saturar la pantalla {RESET}\n")

    for fila in datos[-5:]:
        valores = [str(fila[c]) for c in cabeceras]
        print(" | ".join(valores))
        
    print("------")
    print(f"------ Total de registros cargados: {len(datos)}")
    pausar()

def calcular_estadisticas(datos, cabeceras):

    limpiar_pantalla()
    print(f"{NEGRITA}{AZUL}--- CÁLCULO DE ESTADÍSTICAS DESCRIPTIVAS {RESET}")
    print("--- Columnas disponibles:")
    for i, col in enumerate(cabeceras):
        print(f"{i + 1}. {col}")
        
    try:
        opcion = int(input(f"\n{VERDE}--- Elige el número de la columna numérica a analizar: {RESET}")) - 1
        columna_elegida = cabeceras[opcion]
    
    except (ValueError, IndexError):
        print(f"{ROJO}--- Opción inválida. Debes ingresar un número de la lista.{RESET}")
        pausar()
        return

    valores_numericos = []
    
    for fila in datos:
        valor_crudo = fila[columna_elegida]
        try:
            valor_limpio = float(str(valor_crudo).replace(',', '.'))
            valores_numericos.append(valor_limpio)
        except ValueError:
            continue
            
    if not valores_numericos:
        print(f"{ROJO}--- La columna '{columna_elegida}' no contiene datos numéricos válidos.{RESET}")
        pausar()
        return

    animacion_carga("Calculando estadísticas manualmente")
    
    total_validos = len(valores_numericos)
    promedio = sum(valores_numericos) / total_validos
    
    valores_ordenados = sorted(valores_numericos)
    mitad = total_validos // 2
    if total_validos % 2 == 0:
        mediana = (valores_ordenados[mitad - 1] + valores_ordenados[mitad]) / 2
    else:
        mediana = valores_ordenados[mitad]
        
    maximo = max(valores_numericos)
    minimo = min(valores_numericos)

    print(f"\n{NEGRITA}--- Resultados para la columna '{columna_elegida}':{RESET}")
    print(f"  --- Registros válidos : {total_validos}")
    print(f"  --- Promedio          : {promedio:.2f}")
    print(f"  --- Mediana           : {mediana:.2f}")
    print(f"  --- Valor Máximo      : {maximo}")
    print(f"  --- Valor Mínimo      : {minimo}")
    pausar()

def grafico_tendencia(datos, cabeceras):

    limpiar_pantalla()
    print(f"{NEGRITA}{AZUL}--- GRÁFICO 3: EVOLUCIÓN TEMPORAL / TENDENCIA {RESET}")
    print(f"--- Elige las columnas (idealmente Fecha en X, Valor numérico en Y)")
    
    for i, col in enumerate(cabeceras):
        print(f"{i + 1}. {col}")
        
    try:
        idx_x = int(input(f"\n{VERDE}--- Número de columna para el Eje X (Horizontal): {RESET}")) - 1
        idx_y = int(input(f"{VERDE}--- Número de columna para el Eje Y (Vertical): {RESET}")) - 1
        
        col_x = cabeceras[idx_x]
        col_y = cabeceras[idx_y]
        
        datos_x = [fila[col_x] for fila in datos]
        datos_y = []
        
        for fila in datos:
            try:
                datos_y.append(float(str(fila[col_y]).replace(',', '.')))
            except ValueError:
                datos_y.append(0.0) 
                
        animacion_carga("Generando gráfico de líneas")
        
        plt.figure(figsize=(10, 5))
        plt.plot(datos_x, datos_y, marker='o', color='cyan', linestyle='-', linewidth=2)
        plt.title(f'Tendencia: {col_y} a lo largo de {col_x}', fontsize=14)
        plt.xlabel(col_x)
        plt.ylabel(col_y)
        plt.xticks(rotation=45) 
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        
        nombre_archivo = os.path.join(RUTA_OUTPUTS, f"grafico_tendencia_{col_y}.png")
        plt.savefig(nombre_archivo)
        plt.close() 
        
        print(f"\n{VERDE}--- Gráfico guardado exitosamente en '{nombre_archivo}'{RESET}")
        
    except (ValueError, IndexError):
        print(f"{ROJO}--- Selección inválida.{RESET}")
    pausar()

def grafico_pastel(datos, cabeceras):

    limpiar_pantalla()
    print(f"{NEGRITA}{AZUL}--- GRÁFICO 4: COMPARACIÓN CATEGÓRICA (PASTEL) {RESET}")
    
    for i, col in enumerate(cabeceras):
        print(f"{i + 1}. {col}")
        
    try:
        idx_cat = int(input(f"\n{VERDE}--- Número de columna para la categoría: {RESET}")) - 1
        col_categoria = cabeceras[idx_cat]
        
        conteo = {}
        for fila in datos:
            categoria = fila[col_categoria]
            if categoria == "" or categoria is None:
                categoria = "Sin Dato"
            conteo[categoria] = conteo.get(categoria, 0) + 1
            
        animacion_carga("Generando gráfico de pastel")
        
        etiquetas = list(conteo.keys())
        valores = list(conteo.values())
        
        plt.figure(figsize=(8, 8))
        plt.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.title(f'Comparación Categórica: {col_categoria}', fontsize=14)
        
        nombre_archivo = os.path.join(RUTA_OUTPUTS, f"grafico_pastel_{col_categoria}.png")
        plt.savefig(nombre_archivo)
        plt.close()
        
        print(f"\n{VERDE}--- Gráfico guardado exitosamente en '{nombre_archivo}'{RESET}")
        
    except (ValueError, IndexError):
        print(f"{ROJO}--- Selección inválida.{RESET}")
    pausar()

def grafico_dispersion(datos, cabeceras):

    limpiar_pantalla()
    print(f"{NEGRITA}{AZUL}--- GRÁFICO 5: CORRELACIÓN DE VARIABLES (DISPERSIÓN) {RESET}")
    print(f"--- Elige DOS columnas numéricas para ver su relación.")
    
    for i, col in enumerate(cabeceras):
        print(f"{i + 1}. {col}")
        
    try:
        idx_x = int(input(f"\n{VERDE}--- Número de columna para el Eje X: {RESET}")) - 1
        idx_y = int(input(f"{VERDE}--- Número de columna para el Eje Y: {RESET}")) - 1
        
        col_x = cabeceras[idx_x]
        col_y = cabeceras[idx_y]
        
        datos_x = []
        datos_y = []
        
        for fila in datos:
            try:
                val_x = float(str(fila[col_x]).replace(',', '.'))
                val_y = float(str(fila[col_y]).replace(',', '.'))
                datos_x.append(val_x)
                datos_y.append(val_y)
            except ValueError:
                continue 
                
        animacion_carga("Generando gráfico de dispersión")
        
        plt.figure(figsize=(8, 6))
        plt.scatter(datos_x, datos_y, color='magenta', alpha=0.7, edgecolors='white')
        plt.title(f'Correlación: {col_x} vs {col_y}', fontsize=14)
        plt.xlabel(col_x)
        plt.ylabel(col_y)
        plt.grid(True, linestyle='--', alpha=0.6)
        
        nombre_archivo = os.path.join(RUTA_OUTPUTS, f"grafico_dispersion_{col_x}_vs_{col_y}.png")
        plt.savefig(nombre_archivo)
        plt.close()
        
        print(f"\n{VERDE}--- Gráfico guardado exitosamente en '{nombre_archivo}'{RESET}")
        
    except (ValueError, IndexError):
        print(f"{ROJO}--- Selección inválida.{RESET}")
    pausar()

def grafico_barras_totales(datos, cabeceras):
    
    limpiar_pantalla()

    print(f"{NEGRITA}{AZUL}--- GRÁFICO 6: TOTAL ACUMULADO POR CATEGORÍA {RESET}")
    print("--- Elige una columna categórica (ej. Ciudad) y una numérica (ej. Monto_Venta).")
    
    for i, col in enumerate(cabeceras):
        print(f"{i + 1}. {col}")
        
    try:
        idx_cat = int(input(f"\n{VERDE}--- Número de columna CATEGÓRICA (Eje X): {RESET}")) - 1
        idx_val = int(input(f"{VERDE}--- Número de columna NUMÉRICA (Valor a sumar): {RESET}")) - 1
        
        col_cat = cabeceras[idx_cat]
        col_val = cabeceras[idx_val]
        
        sumas = {}
        
        for fila in datos:
            categoria = fila[col_cat]
            try:
                valor = float(str(fila[col_val]).replace(',', '.'))
                sumas[categoria] = sumas.get(categoria, 0.0) + valor
            except ValueError:
                continue 
                
        animacion_carga("Generando gráfico de barras de totales")
        
        etiquetas = list(sumas.keys())
        valores = list(sumas.values())
        
        plt.figure(figsize=(10, 6))
        plt.bar(etiquetas, valores, color='#2ecc71', edgecolor='white')
        plt.title(f'Total Acumulado de {col_val} por {col_cat}', fontsize=14)
        plt.xlabel(col_cat)
        plt.ylabel(f'Suma Total de {col_val}')
        
        for i, v in enumerate(valores):
            plt.text(i, v + (v * 0.02), f"{v:,.0f}", ha='center', color='white', fontweight='bold')
            
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        
        nombre_archivo = os.path.join(RUTA_OUTPUTS, f"grafico_barras_totales_{col_cat}.png")
        plt.savefig(nombre_archivo)
        plt.close()
        print(f"\n{VERDE}--- Gráfico guardado exitosamente en '{nombre_archivo}'{RESET}")
    
    except (ValueError, IndexError):
        print(f"{ROJO}--- Selección inválida.{RESET}")
    
    pausar()

def grafico_boxplot(datos, cabeceras):
    
    limpiar_pantalla()
    
    print(f"{NEGRITA}{AZUL}--- GRÁFICO 7: DIAGRAMA DE CAJA (BOXPLOT) {RESET}")
    print("--- Muestra dónde se concentran los datos y si hay valores atípicos.")
    
    for i, col in enumerate(cabeceras):
        print(f"{i + 1}. {col}")
        
    try:
        idx_val = int(input(f"\n{VERDE}--- Elige la columna NUMÉRICA a analizar: {RESET}")) - 1
        col_val = cabeceras[idx_val]
        
        datos_numericos = []
        
        for fila in datos:
            try:
                datos_numericos.append(float(str(fila[col_val]).replace(',', '.')))
            except ValueError:
                continue
                
        if not datos_numericos:
            print(f"{ROJO}--- No hay datos numéricos válidos en esta columna.{RESET}")
            pausar()
            return
            
        animacion_carga("Generando Boxplot")
        
        plt.figure(figsize=(8, 6))
        caja = plt.boxplot(datos_numericos, patch_artist=True)
        
        for element in ['boxes', 'whiskers', 'fliers', 'caps', 'medians']:
            plt.setp(caja[element], color='#e67e22', linewidth=2)
        
        plt.setp(caja['boxes'], facecolor='#d35400', alpha=0.5)
        
        plt.title(f'Distribución y Valores Atípicos: {col_val}', fontsize=14)
        plt.ylabel(col_val)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        
        nombre_archivo = os.path.join(RUTA_OUTPUTS, f"grafico_boxplot_{col_val}.png")
        plt.savefig(nombre_archivo)
        plt.close()
        print(f"\n{VERDE}--- Gráfico guardado exitosamente en '{nombre_archivo}'{RESET}")
    
    except (ValueError, IndexError):
        print(f"{ROJO}--- Selección inválida.{RESET}")
    
    pausar()


def menu_analisis_csv():
    
    limpiar_pantalla()
    print(f"{NEGRITA}{AZUL}--- MÓDULO DE ANÁLISIS DE DATASET (.CSV) {RESET}")
   
    ruta_defecto = os.path.join(DIRECTORIO_BASE, "Data", "ventas.csv")
    ruta = input(f"{VERDE}--- Ingresa la ruta del archivo CSV (Enter para usar '{ruta_defecto}'): {RESET}").strip()
    if not ruta:
        ruta = ruta_defecto 
        
    animacion_carga("Cargando y parseando archivo CSV")
    datos, cabeceras = cargar_datos_csv(ruta)
    
    if not datos:
        pausar()
        return 

    while True:
        limpiar_pantalla()
        print(f"{NEGRITA}------ ANÁLISIS CSV: {os.path.basename(ruta)}{RESET}")
        print(f"--- 1. Ver vista previa de los datos (Top 10 / Bottom 5)")
        print(f"--- 2. Calcular estadísticas de una columna")
        print(f"--- 3. Generar Gráfico de Tendencia (Líneas)")
        print(f"--- 4. Generar Gráfico de Categorías (Pastel)")
        print(f"--- 5. Generar Gráfico de Correlación (Dispersión)")
        print(f"--- 6. Generar Gráfico de Barras (Total por Categoría)")
        print(f"--- 7. Generar Gráfico de Caja (Boxplot)")
        print(f"{ROJO}--- 8. Volver al menú principal{RESET}")
        
        opcion = input(f"\n{AZUL}--- Elige una opción (1-8): {RESET}").strip()
        
        if opcion == '1':
            mostrar_vista_previa(datos, cabeceras)
        
        elif opcion == '2':
            calcular_estadisticas(datos, cabeceras)
        
        elif opcion == '3':
            grafico_tendencia(datos, cabeceras)
        
        elif opcion == '4':
            grafico_pastel(datos, cabeceras)
        
        elif opcion == '5':
            grafico_dispersion(datos, cabeceras)
            
        elif opcion == '6':
            grafico_barras_totales(datos, cabeceras)
            
        elif opcion == '7':
            grafico_boxplot(datos, cabeceras)
        
        elif opcion == '8':
            break
        
        else:
            print(f"{ROJO}--- Opción no válida.{RESET}")
            pausar()