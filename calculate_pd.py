import pandas as pd
from math import sqrt

def total_way(dataPD):

    wayX = 0
    wayY = 0
    total = 0

    for IndexEl in range(1, len(dataPD)):

        deltaX = abs(dataPD['Ax'][IndexEl] - dataPD['Ax'][IndexEl-1])
        deltaY = abs(dataPD['Ay'][IndexEl] - dataPD['Ay'][IndexEl-1])

        wayX += deltaX
        wayY += deltaY

        way_element = sqrt(deltaX ** 2 + deltaY ** 2)
        total += way_element

    return {'wayX': round(wayX, 2), 'wayY': round(wayY, 2), 'total_way': round(total, 2)}
