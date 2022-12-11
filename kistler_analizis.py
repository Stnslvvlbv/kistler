import matplotlib.pyplot as plt

from read_file_pd import readFile
from calculate_pd import total_way

class kistler():

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

    def paint_track(self):
      


        self.freshdata.plot(x='Ax', y='Ay', xlabel='M-L (мм)', ylabel='A-P (мм)', label='COP')
        plt.show()




test = kistler('sample.txt')
print(test.total)
print(test.average)
print(test.standart_deviation)
test.paint_track()
