import cv2
import tensorflow as tf
import numpy as np
from  keras.models import load_model


rostro_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Cargar un modelo preentrenado de reconocimiento de emociones
modelo_emociones = load_model("haarcascade_frontalface_default.xml")  

captura = cv2.VideoCapture(1)

while True:
    _, img = captura.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    rostros = rostro_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
    
    for (x, y, w, h) in rostros:
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48))  # Ajustar el tamaño según el modelo de emociones
        
        # Normalizar la imagen y agregar una dimensión adicional para el canal de color
        roi_gray = roi_gray / 255.0
        roi_gray = np.expand_dims(roi_gray, axis=0)
        roi_gray = np.expand_dims(roi_gray, axis=-1)

        # Realizar la predicción usando el modelo de emociones
        emociones_prediccion = modelo_emociones.predict(roi_gray)
        
        # Obtener la emoción con mayor probabilidad
        emocion_index = np.argmax(emociones_prediccion)
        emociones_labels = ["Enojo", "Disgusto", "Miedo", "Feliz", "Tristeza", "Sorpresa", "Neutral"]
        emocion = emociones_labels[emocion_index]

        # Dibujar un rectángulo alrededor del rostro
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Mostrar la emoción detectada
        cv2.putText(img, emocion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("img", img)
    salida = cv2.waitKey(30)
    if salida == 27:
        break

captura.release()
cv2.destroyAllWindows()
