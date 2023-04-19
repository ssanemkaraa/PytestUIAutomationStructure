import cv2
import numpy as np
from PIL import ImageGrab

# Ekranı sürekli olarak izler ve kenarları algılayarak gösterir

while True:
    screen = np.array(ImageGrab.grab(bbox=None))
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 50, 150)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    closed = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)
    contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(screen, (x,y), (x+w,y+h), (0,255,255), 5)
        # Görüntüyü göster
    cv2.imshow('image', screen)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('son_goruntu.png', screen)
        break