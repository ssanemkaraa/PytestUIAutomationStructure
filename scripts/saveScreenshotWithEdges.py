import numpy as np
import cv2
from PIL import ImageGrab

# Ekran görüntüsü al
screen = np.array(ImageGrab.grab(bbox=None))

# Görüntüyü gri tonlamalı hale getir
gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
colory = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

# Kenar algılama filtresi uygula
canny = cv2.Canny(gray, 100, 150)

# Morfolojik kapanma işlemi uygula
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
closed = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)

# Konturları bul
contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Görüntü üzerindeki her bir kontur için dikdörtgen çiz
for contour in contours:
    (x,y,w,h) = cv2.boundingRect(contour)
    cv2.rectangle(screen, (x,y), (x+w,y+h), (255,255,0), 10)
    colory = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

cv2.imwrite('son_goruntu.png', colory)
