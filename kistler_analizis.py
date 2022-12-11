import matplotlib.pyplot as plt
import pandas as pd

from read_file_pd import readFile
from calculate_pd import total_way

class Kistler():

    def __init__(self, url):
        self.url = url
        self.freshdata = readFile(url)
        self.total = total_way(self.freshdata)
        self.average = {
            'averageX (мм)': round(self.freshdata['Ax'].mean(), 2),
            'averedeY (мм)': round(self.freshdata['Ay'].mean(), 2),
        }
        self.standart_deviation = {
            'stdX (мм)': round(self.freshdata['Ax'].std(), 2),
            'stdY (мм)': round(self.freshdata['Ay'].std(), 2),
        }

    def paint_track(self, step=1, x='Ax', y='Ay'):
        poligon_paint = []
        for elIndex in range(0,len(self.freshdata)):

            if elIndex % step == 0:
                corner_paint = [self.freshdata[x][elIndex], self.freshdata[y][elIndex]]
                poligon_paint.append(corner_paint)
        data_paint = pd.DataFrame(poligon_paint, index=None, columns=[x, y])

        data_paint.plot(x=x, y=y, xlabel='M-L (мм)', ylabel='A-P (мм)', label='COP')
        plt.show()




test = Kistler('sample.txt')
print(test.total)
print(test.average)
print(test.standart_deviation)
test.paint_track(step=5)
