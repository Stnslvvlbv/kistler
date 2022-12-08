import numpy as np
import cv2


def paint(data, shift=1):
    height = 700
    width = 700
    img = np.zeros((width, height, 3), np.uint8)
    cv2.rectangle(img, (0, 0), (width, height), (255, 255, 255), -1)

    poligon = []
    for el in data:
        X_next = el[shift]*10 - width / 2
        Y_next = el[shift+1]*10 - height / 2

        corner = [X_next, Y_next]
        poligon.append(corner)

    pts = np.array(poligon,  np.int64)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(img, [pts], False, (0, 255, 255))

    cv2.imshow("Image", img)
    cv2.waitKey(0)

# paint(data)
