import pyautogui
from PIL import Image, ImageDraw

im = pyautogui.screenshot()

draw = ImageDraw.Draw(im)

width, height = im.size

interval = 50

for i in range(0, width, interval):
    draw.line([(i, 0), (i, height)], fill='red', width=2)

for i in range(0, height, interval):
    draw.line([(0, i), (width, i)], fill='blue', width=2)

im.save('screenshot_with_grid.png')
