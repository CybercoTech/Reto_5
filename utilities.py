# utilities.py

import os
import sys
import time


VERDE = '\033[92m'
AMARILLO = '\033[93m'
ROJO = '\033[91m'
AZUL = '\033[94m'
CIAN = '\033[96m'
NEGRITA = '\033[1m'
RESET = '\033[0m'

def limpiar_pantalla():

    if os.name == 'nt': # Windows
        os.system('cls')

    else: # Mac/Linux
        os.system('clear')

def pausar():

    input(f"\n{AMARILLO}Presiona Enter para continuar...{RESET}")

def mostrar_banner():

    print(f"""{AZUL}{NEGRITA} ------ EXPLORADOR CLI PARA ANÁLISIS DE DATOS REALES {RESET}""")

def animacion_carga(mensaje="Procesando", segundos=1.5):
    
    print(f"{CIAN}{mensaje}", end="", flush=True)

    for _ in range(3):
        time.sleep(segundos / 3)
        print(".", end="", flush=True)

    print(f" ¡Listo!{RESET}")
    time.sleep(0.5)

def formatear_tamano(bytes):
   
    if bytes < 1024:
        return f"{bytes} bytes"
    
    elif bytes < 1024 * 1024:
        return f"{bytes / 1024:.2f} KB"
    
    else:
        return f"{bytes / (1024 * 1024):.2f} MB"

def validar_ruta(ruta):
    if os.path.exists(ruta):

        return True
    
    return False