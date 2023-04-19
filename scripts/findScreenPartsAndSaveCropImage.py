import numpy as np
import cv2
from PIL import ImageGrab
import json
import pytesseract
import os
import AppKit

# Ekran görüntüsünden bilgi çıkarmak için kullanılan bir görüntü işleme ve metin okuma aracıdır.
# Kod, Pytesseract adlı bir Python kütüphanesi kullanarak, görüntü üzerindeki metinleri okuyarak,
# dikdörtgenler içine alır ve bir JSON dosyasında kaydeder. Kod, OpenCV (cv2) kütüphanesi ile görüntü işleme
# işlemleri gerçekleştirir.
#
# Ekran görüntüsü alınır ve gri tonlamalı hale getirilir.
# Kenar algılama filtresi (Canny) uygulanır ve morfolojik kapanma işlemi ile görüntü iyileştirilir.görüntü üzerindeki
# nesnelerin kenarları daha belirgin hale gelir.
#
# Konturlar bulunur ve dikdörtgenler çizilir.
# Görüntü üzerindeki her bir dikdörtgen için, Pytesseract
# kütüphanesi kullanılarak metin okunur ve JSON dosyasına kaydedilir.
# Her bir dikdörtgen için bir görüntü dosyası oluşturulur.
#
# İşlenmiş görüntü ve JSON dosyası kaydedilir.

shape_level = 80
canny_level_1 = 100
canny_level_2 = 500
resultScreenPath = f"{os.getcwd()}/scripts/resultData/mainData/resultImage.png"
resultJsonPath = f"{os.getcwd()}/scripts/resultData/mainData/data.json"
imagePartsPath = f"{os.getcwd()}/scripts/resultData/detailData/part"

screen = np.array(ImageGrab.grab(bbox=None))

# Ana ekranın boyutunu al
screen_width = ImageGrab.grab().width
screen_height = ImageGrab.grab().height

print("height "+str(screen_height))
print("width "+str(screen_width))


# Ana ekranın üstten ve alttan kesilecek yüzdesi
cut_top = int(screen_width * 0.06)
cut_bottom = int(screen_height * 0.06)

# Ana ekranın kesilmiş koordinatları
bbox = (0, 20, screen_width, screen_height)

print(bbox)

# Ekran görüntüsü al
screen = np.array(ImageGrab.grab(bbox=None))

# Görüntüyü gri tonlamalı hale getir
gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
colory = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

# Kenar algılama filtresi uygula
canny = cv2.Canny(gray, canny_level_1, canny_level_2)

# Otomatik kernel boyutunu belirle
kernel_size = int(min(canny.shape) / shape_level)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))

# Morfolojik kapanma işlemi uygula
closed = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)

# Konturları bul
contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Görüntü üzerindeki her bir kontur için dikdörtgen çiz, koordinatları ve metni kaydet
data = []
id_counter = 1
for contour in contours:
    (x, y, w, h) = cv2.boundingRect(contour)
    cv2.rectangle(screen, (x, y), (x + w, y + h), (255, 255, 0), 1)
    colory = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    text = pytesseract.image_to_string(screen[y:y + h, x:x + w], lang='eng')  # dikdörtgen içindeki metni oku

    data.append({"id": id_counter, "text": text, "coordinates": {"x": x, "y": y, "width": w, "height": h}})

    # Dikdörtgenin koordinatları
    # (x, y, w, h) = cv2.boundingRect(contour)

    # # Metnin boyutunu al
    # (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=1)
    # # Metni dikdörtgenin ortasına yerleştir
    # text_x = int(x + (w - text_width) / 2)
    # text_y = int(y + (h + text_height) / 2)
    # cv2.putText(screen, str(id_counter), (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0), thickness=3)

    # Kayıt yolunu oluştur ve png olarak kaydet
    cv2.imwrite(imagePartsPath + f"_{text}.png", colory[y:y + h, x:x + w])

    # Kayıt yolunu JSON dosyasına kaydet
    data[-1]['save_path'] = imagePartsPath + f"_{id_counter}.png"

    id_counter += 1

cv2.imwrite(resultScreenPath, colory)

# JSON dosyasına verileri kaydet
with open(resultJsonPath, 'w') as outfile:
    json.dump(data, outfile)
