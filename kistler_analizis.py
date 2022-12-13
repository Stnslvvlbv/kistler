import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

import pandas as pd
from math import sqrt

from plot_confidence_ellipse import confidence_ellipse
from read_file_pd import readFile
from calculate_pd import total_way, name_cuter, square
# from princ_comp_analysis import princ_comp_analysis

class Kistler():

    def __init__(self, url):
        WINDOW = 35
        self.url = url.replace('\\', '/')
        self.freshdata = readFile(self.url, WINDOW)
        self.name = name_cuter(self.url)
        self.total = total_way(self.freshdata)
        self.average = {
            'averageX (мм)': round(self.freshdata['Ax'].mean(), 2),
            'averageY (мм)': round(self.freshdata['Ay'].mean(), 2),
        }

        self.covariance_matrix = self.freshdata[['Ax', 'Ay']].cov()
        self.pearson = self.covariance_matrix.iloc[0, 1] / sqrt(self.covariance_matrix.iloc[0, 0] * self.covariance_matrix.iloc[1, 1])

        self.standart_deviation = {
            'stdX (мм)': round(self.freshdata['Ax'].std(), 2),
            'stdY (мм)': round(self.freshdata['Ay'].std(), 2),
        }

        sqr = square(self.freshdata, self.average)
        self.square = round(sqr['square'], 2)
        self.square_points = sqr['square_points']


    def square_track(self):
        sqr=square(self.freshdata, self.average)
        self.square = round(sqr['square'], 2)
        self.points = sqr['square_points']
        points.plot(x='Ax', y='Ay', xlabel='M-L (мм)', ylabel='A-P (мм)', label='COP')
        # plt.show()


    def  principal_component_analysis(self):
        princ_comp_analysis(self.freshdata, self.standart_deviation)

    def paint_track(self, step=1, x='Ax', y='Ay'):
        poligon_paint = []
        for elIndex in range(0, len(self.freshdata), step):
            corner_paint = [self.freshdata[x][elIndex], self.freshdata[y][elIndex]]
            poligon_paint.append(corner_paint)

        data_paint = pd.DataFrame(poligon_paint, index=None, columns=[x, y])

        # self.square_points.plot(x='Ax', y='Ay', xlabel='M-L (мм)', ylabel='A-P (мм)', label='square')
        x0 = self.average['averageX (мм)']
        y0 = self.average['averageY (мм)']
        point_average = [
            [x0, x0+0.001],
            [y0, y0+0.001]
        ]
        data_paint.plot(x=x, y=y, xlabel='M-L (мм)', ylabel='A-P (мм)', label='COP')
        plt.plot(
            self.square_points['Ax'], self.square_points['Ay'],
            label='square',
            color = (1, 0, 0, 0.2),
            linewidth=6,
        )
        plt.plot(point_average[0], point_average[1], color=(1, 0, 0, 0.4),linewidth=6,)
        plt.title("")
        plt.show()


    def elipce(self, n_std=3):
        x = 'Ax'
        y = 'Ay'
        X = self.freshdata[['Ax']].to_numpy()

        poligon_paint = []
        for elIndex in range(0, len(self.freshdata), 1):
            corner_paint = [self.freshdata[x][elIndex], self.freshdata[y][elIndex]]
            poligon_paint.append(corner_paint)

        data_paint = pd.DataFrame(poligon_paint, index=None, columns=[x, y])

        ax = data_paint.plot(x=x, y=y, xlabel='M-L (мм)',
            color=(0, 0, 1, 1), ylabel='A-P (мм)', label='COP')

        plt.plot(
            self.square_points['Ax'], self.square_points['Ay'],
            label='square',
            color=(1, 0, 0, 0.2),
            linewidth=6,
        )

        plt.scatter(self.average['averageX (мм)'], self.average['averageY (мм)'])

        ellipse = confidence_ellipse(
            self.covariance_matrix,
            self.average,
            ax=ax
        )


        # ax.add_patch(ellipse)
        plt.show()

test = Kistler('sample.txt')
print(test.total)
print(test.average)
print(test.standart_deviation)
# test.paint_track(step=1)
# test.principal_component_analysis()
test.elipce()
print(test.square)
#-0.6041877416129416