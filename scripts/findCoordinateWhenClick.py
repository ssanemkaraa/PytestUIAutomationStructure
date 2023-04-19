import numpy as np
import pytesseract
from PIL import ImageGrab
from pynput import mouse


def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        print('Fare imleci koordinatları: x={}, y={}'.format(x, y))

        # monitor = {"top": y, "left": x, "width": 100, "height": 100}
        # img = np.array(ImageGrab.grab(monitor))
        # text = pytesseract.image_to_string(img, lang='eng')
        # print('Fare imlecindeki metin: {}'.format(text))


with mouse.Listener(on_click=on_click) as listener:
    listener.join()
