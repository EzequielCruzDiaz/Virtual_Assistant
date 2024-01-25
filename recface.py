import cv2

rostro = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

captura = cv2.VideoCapture(0)

while True:
    _, img = captura.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.1, 4)
    for (x,y,w,h) in rostros:
        cv2.rectangle(img,(x, y), (x+w, y+h),(255, 0, 0), 2)
    cv2.imshow("img", img)
    salida = cv2.waitKey(30)
    if salida == 27:
        break
captura.release()