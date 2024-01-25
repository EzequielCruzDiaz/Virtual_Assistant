import pyjokes
import pyttsx3
import pywhatkit
import wikipedia, webbrowser
import datetime
import time
import speech_recognition as sr
import yfinance as yf
import subprocess
import pyautogui
from pathlib import Path

usuario = "Ezequiel" 
voz = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-MX_SABINA_11.0"



def transformar_audio_texto():
    r = sr.Recognizer()
    with sr.Microphone() as origen:
        r.pause_threshold = 0.8
        print("ya puedes hablar")  
        audio = r.listen(origen)

        try:
            pedido = r.recognize_google(audio, language="es-mx")
            print("Dijiste: " + pedido)
            return pedido
        
        except sr.UnknownValueError:
            print("Uis... No entendi")
            hablar("Disculpa, no te he entendido")
            return "sigo esperando"

        except sr.RequestError:
            print(f"Uis... No hay servicio")
            return "sigo esperando"

        except:
            print("Uis... Algo salio mal")
            return "sigo esperando"

def hablar(mensaje):
    engine = pyttsx3.init()
    engine.setProperty("voice", voz)
    engine.say(mensaje)
    engine.runAndWait()

def pedir_dia():

    dia = datetime.datetime.today()
    print(dia)

    dia_semana = dia.weekday()
    mes_actual = dia.month
    print(dia_semana)

    calendario = {0: "Lunes",
                  1: "Martes",
                  2: "Miércoles",
                  3: "Jueves",
                  4: "Viernes",
                  5: "Sábado",
                  6: "Domingo"}

    meses = {1: "Enero",
             2: "Febrero",
             3: "Marzo",
             4: "Abril",
             5: "Mayo",
             6: "Junio",
             7: "Julio",
             8: "Agosto",
             9: "Septiembre",
             10: "Octubre",
             11: "Noviembre",
             12: "Diciembre"}

    hablar(f"Hoy es {calendario[dia_semana]} {dia.day} de {meses[mes_actual]}")

def pedir_hora():
    hora = datetime.datetime.now()
    hora = f" En este momento son las {hora.hour} horas con {hora.minute} minutos"
    print(hora)
    hablar(hora)

def saludo_inicial():
    hora_actual = datetime.datetime.now()

    if 6 <= hora_actual.hour < 12:
        momento = f"Buenos días{usuario}"
    elif 12 <= hora_actual.hour < 18:
        momento = f"Buenas Tardes{usuario}"
    else:
        momento = f"Buenas noches{usuario}"

    hablar(f"{momento}, Soy harmony, tu asistente virtual, veo que hoy estas feliz, ")
    mensaje_opciones = "Cuentas con un menú interactivo. Elige a gusto"
    hablar(mensaje_opciones)

def pedir_aplicacion():

    lista_rutas = []
    lista_nombres = []
    ruta = Path("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs")

    for app in ruta.glob("**/*.lnk"):
        lista_rutas.append(app)
        lista_nombres.append(app.stem.lower())

    return lista_nombres, print( lista_rutas)

def abrir_aplicacion(pedido, nombres, rutas):

    correcto = False
    indice_ruta_seleccionada = nombres.index(pedido)

    while not correcto:

        if pedido in nombres:

            aplicacion = rutas[indice_ruta_seleccionada]
            subprocess.Popen(fr'{aplicacion}', shell=True)
            correcto = True

        else:
            hablar('No he encontrado esa aplicación. Inténtalo otra vez')

def abrir_navegador(pedido):
    subprocess.Popen(fr'start opera {pedido}', shell=True)

def pedir_cosas():
    saludo_inicial()

    comenzar = True
    while comenzar:

        print("\nSelecciona una Opcion:")
        print("1. Buscar en Internet")
        print("2. Abrir aplicacion")
        print("3. Buscar Noticias")
        print("4. Pedir la fecha")
        print("5. Pedir la hora")
        print("6. Buscar en wikipedia")
        print("7. Reproducir musica")
        print("8. Contar un chiste")
        print("9. Enviar un mensaje")
        print("10. Salir")

        pedido = input("Opcion:")
        hablar(input)

        if pedido == "1":
            hablar("Ya mismo estoy en eso")
            pedido = pedido.replace("busca en internet", "")
            pywhatkit.search(pedido)
            hablar("Esto es lo que he encontrado")
            continue

        elif pedido == "2":
            nombres, rutas = pedir_aplicacion()
            hablar("Muy bien, qué aplicación deseas abrir?")
            pedido = transformar_audio_texto().lower()
            hablar(f"Abriendo {pedido}")
            abrir_aplicacion(pedido, nombres, rutas)
            continue   
        

        elif pedido == "3":
            webbrowser.open("https://www.diariolibre.com")
        
        elif pedido == "4":
            pedir_dia()
            continue

        elif pedido == "5":
            pedir_hora()
            continue

        elif pedido == "6":
            hablar("Buscando en wikipedia")
            pedido = pedido.replace("wikipedia", '')
            wikipedia.set_lang("es")
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar("Wikipedia dice los siguiente:")
            hablar(resultado)
            continue

        elif pedido == "7":
            pywhatkit.playonyt(pedido)
            continue

        elif pedido == "8":
            hablar(pyjokes.get_joke("es"))
            continue


        elif pedido == "9":
            hablar("Enviando el mensaje")
            mensaje = pedido.split("diga")[-1].strip()
            pywhatkit.sendwhatmsg_instantly("+18299673641", mensaje)
            time.sleep(5)
            pyautogui.press("enter")
            continue

        elif pedido == "10":
            hablar("claro, ya sabes donde encontrarme")
            comenzar = False
    
        else:
            hablar("Lo siento, no entiendo esa opcion.Por favor, selecciona una opción válida.")

pedir_cosas()
