import pyjokes
import pyttsx3
import pywhatkit
import wikipedia
import webbrowser
import datetime
import time
import speech_recognition as sr
import subprocess
import pyautogui
import threading
import openai
from pathlib import Path

openai.api_key = "YOUR API KEY"
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
            print("Uis... No entendí")
            hablar("Disculpa, no te he entendido")
            return "sigo esperando"

        except sr.RequestError:
            print(f"Uis... No hay servicio")
            return "sigo esperando"

        except:
            print("Uis... Algo salió mal")
            return "sigo esperando"

def obtener_respuesta(pregunta):
    try:
        respuesta_creada = openai.completions.create(
            engine = "text-davinci-002",
            prompt=pregunta,
            max_tokens=150
            
        )
        return respuesta_creada.choices[0].text.strip()
    
    except  Exception as e:
        print(f"Error al obtener respuesta{e}")
        return "Lo siento, hubo un error al procesar tu solicitud"

def buscar_en_internet(pedido):
    hablar("ya mismo estoy en eso")
    pedido = pedido.replace("buscar en internet")
    threading.Thread(target=buscar_en_internet_thread, args=(pedido,)).start()

def buscar_en_internet_thread(pedido):
    pywhatkit.search(pedido)
    hablar("Esto es lo que he encontrado")

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

    calendario = {
        0: "Lunes",
        1: "Martes",
        2: "Miércoles",
        3: "Jueves",
        4: "Viernes",
        5: "Sábado",
        6: "Domingo",
    }

    meses = {
        1: "Enero",
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
        12: "Diciembre",
    }

    hablar(f"Hoy es {calendario[dia_semana]} {dia.day} de {meses[mes_actual]}")

def pedir_hora():
    hora = datetime.datetime.now()
    hora = f" En este momento son las {hora.hour} horas con {hora.minute} minutos"
    print(hora)
    hablar(hora)

def pedir_informacion():
    hablar("Hola, ¿Cómo te llamas?")
    nombre = transformar_audio_texto()
    hablar(f"¡Hola {nombre}! ¿Cómo te sientes hoy?")
    animo = transformar_audio_texto()
    return nombre, animo

def saludo_inicial(nombre, animo):
    hora_actual = datetime.datetime.now()

    if 6 <= hora_actual.hour < 12:
        momento = f"Buenos días {nombre}"
    elif 12 <= hora_actual.hour < 18:
        momento = f"Buenas Tardes {nombre}"
    else:
        momento = f"Buenas noches {nombre}"

    hablar(f"{momento}, Soy harmony, tu asistente virtual.")
    
    if animo.lower() in ["muy bien" , "bien" , "excelente"]:
        return hablar(f"Excelente escuchar eso {nombre}, que deseas hacer para continuar con este grandioso dia ")
    
    elif animo.lower()  in ["triste" , "mal"]:
        return hablar(f"lamento que te encuentres {animo}, vamos a escuchar tu musica favorita o iniciar la app que te gusta, para subir ese animo")
    
    else:
        hablar(f"Desplegare el menu de opciones.")

def pedir_aplicacion():
    lista_rutas = []
    lista_nombres = []
    ruta = Path("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs")

    for app in ruta.glob("**/*.lnk"):
        lista_rutas.append(app)
        lista_nombres.append(app.stem.lower())

    return lista_nombres, lista_rutas

def abrir_aplicacion(pedido, nombres, rutas):
    try:
        indice_ruta_seleccionada = nombres.index(pedido)
        aplicacion = rutas[indice_ruta_seleccionada]
        threading.Thread(target=abrir_aplicacion_thread, args=(aplicacion,)).start()
    except ValueError:
        hablar("No he encontrado esa aplicación. Inténtalo otra vez")

def abrir_aplicacion_thread(aplicacion):
    subprocess.Popen(fr'"{aplicacion}"', shell=True)

def abrir_navegador(pedido):
    subprocess.Popen(fr'start opera {pedido}', shell=True)

def pedir_cosas():
    nombre, animo = pedir_informacion()
    saludo_inicial(nombre, animo)

    comenzar = True
    while comenzar:
        print("\nSelecciona una Opcion:")
        print("1. Buscar en Internet")
        print("2. Abrir aplicación")
        print("3. Buscar Noticias")
        print("4. Pedir la fecha")
        print("5. Pedir la hora")
        print("6. Buscar en Wikipedia")
        print("7. Reproducir música")
        print("8. Contar un chiste")
        print("9. Enviar un mensaje")
        print("10. Salir")

        pedido = transformar_audio_texto()

        if "internet" in pedido:
           buscar_en_internet(pedido)
           continue

        elif "aplicación" in pedido:
            nombres, rutas = pedir_aplicacion()
            hablar("Muy bien, ¿qué aplicación deseas abrir?")
            pedido = transformar_audio_texto().lower()
            hablar(f"Abriendo {pedido}")
            abrir_aplicacion(pedido, nombres, rutas)
            continue

        elif "noticias" in pedido:
            webbrowser.open("https://www.diariolibre.com")

        elif "fecha" in pedido:
            pedir_dia()
            continue

        elif "hora" in pedido:
            pedir_hora()
            continue

        elif "wikipedia" in pedido:
            hablar("Buscando en Wikipedia")
            pedido = pedido.replace("wikipedia", "")
            wikipedia.set_lang("es")
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar("Wikipedia dice lo siguiente:")
            hablar(resultado)
            continue

        elif "reproduce" in pedido:
            pywhatkit.playonyt(pedido)
            continue

        elif "chiste" in pedido:
            hablar(pyjokes.get_joke("es"))
            continue

        elif "mensaje" in pedido:
            hablar("Enviando el mensaje")
            mensaje = transformar_audio_texto().split("diga")[-1].strip()
            pywhatkit.sendwhatmsg_instantly("+18299673641", mensaje)
            time.sleep(5)
            pyautogui.press("enter")
            continue

        elif "Eso es todo" in pedido:
            hablar("Claro, ya sabes donde encontrarme")
            comenzar = False

        else:
            hablar("Lo siento, no entiendo esa opción. Por favor, selecciona una opción válida.")

pedir_cosas()
