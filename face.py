
import cv2
import numpy as np
from alive_progress import alive_bar
from colorspacious import cspace_convert


def cvt(color, lab):
    global bar
    bar()
    l, a, b = lab
    color = cspace_convert(color, 'sRGB255', 'CIELab')
    color[0] *= l
    color[1] *= a
    color[2] *= b
    color = cspace_convert(color, 'CIELab', 'sRGB255')
    bar()
    return color


labs = [
    [1.0356, 0.9823, 1.005],
    [1.012, 0.8255, 0.9323],
    [1.034, 0.9058, 0.978],
    [1.127, 0.8725, 0.9644],
]


def worker(i):
    img = cv2.imread(f'faces/p{i+1}.png')
    img = cv2.resize(img, (400, 400))
    img = np.array([[cvt(pixel, labs[i]) for pixel in row] for row in img])
    cv2.imwrite(f'faces-new/p{i+1}.jpg', img)



with alive_bar(400**2*4, ctrl_c=True, title=f'渲染图片') as _bar:
    global bar
    bar = _bar
    for i in range(4):
        worker(i)
