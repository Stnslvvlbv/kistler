import matplotlib.pyplot as plt

from math import sqrt

from plot_confidence_ellipse import confidence_ellipse
from read_file_pd import readFile
from calculate_pd import total_way, name_cuter, square


def track_fresh(dataPD, average, x='Ax', y='Ay'):
    ax = dataPD.plot(x=x, y=y, xlabel='M-L (мм)', ylabel='A-P (мм)', label='COP')
    plt.scatter(average['averageX (мм)'], average['averageY (мм)'], color=(0.9, 0.1, 0.1, 0.5), lw=3)
    return ax


class Kistler:
    def __init__(self, url):
        WINDOW = 35
        self.square = None
        self.ellipse_square = None
        self.url = url.replace('\\', '/')
        self.fresh_data = readFile(self.url, window=WINDOW)
        self.name = name_cuter(self.url)
        self.total = total_way(self.fresh_data)
        self.average = {
            'averageX (мм)': self.fresh_data['Ax'].mean(),
            'averageY (мм)': self.fresh_data['Ay'].mean(),
        }

        self.covariance_matrix = self.fresh_data[['Ax', 'Ay']].cov()
        self.pearson = self.covariance_matrix.iloc[0, 1] / sqrt(
            self.covariance_matrix.iloc[0, 0] * self.covariance_matrix.iloc[1, 1])

        self.standard_deviation = {
            'stdX (мм)': self.fresh_data['Ax'].std(),
            'stdY (мм)': self.fresh_data['Ay'].std(),
        }


    def track_paint(self):
        track_fresh(self.fresh_data, self.average)

        plt.show()


    def square_track(self):

        track_fresh(self.fresh_data, self.average)

        sqr = square(self.fresh_data, self.average)
        self.square = round(sqr['square'], 2)

        plt.plot(
            sqr['square_points']['Ax'], sqr['square_points']['Ay'],
            label='square',
            color=(1, 0, 0, 0.2),
            linewidth=6,
        )
        plt.show()


    def ellipse(self, path_image, n_std=1.96):

        ax = track_fresh(self.fresh_data, self.average)

        ellipse = confidence_ellipse(
            self.covariance_matrix,
            self.average,
            n_std=n_std,
            ax=ax
        )

        self.ellipse_square = round(ellipse['square'], 2)
        # var = ellipse['plot']

        # plt.savefig(path_image + '/' + self.name)
        # plt.show()


class KistlerForSQL(Kistler):
    def __init__(self, dataPD):
        WINDOW = 35
        self.square = None
        self.ellipse_square = None

        self.fresh_data = dataPD.rolling(WINDOW, min_periods=1).mean()

        # self.name = name_cuter(self.url)
        self.total = total_way(self.fresh_data)
        self.average = {
            'averageX (мм)': self.fresh_data['Ax'].mean(),
            'averageY (мм)': self.fresh_data['Ay'].mean(),
        }

        self.covariance_matrix = self.fresh_data[['Ax', 'Ay']].cov()
        self.pearson = self.covariance_matrix.iloc[0, 1] / sqrt(
            self.covariance_matrix.iloc[0, 0] * self.covariance_matrix.iloc[1, 1])

        self.standard_deviation = {
            'stdX (мм)': self.fresh_data['Ax'].std(),
            'stdY (мм)': self.fresh_data['Ay'].std(),
        }

"""
test = Kistler('D:/pr/kistler/data/Stabila_records/ST013/ST013_ts_EO 001.txt')
print(test.total)
print(test.average)
print(test.standard_deviation)
test.track_paint()

test.ellipse('jjj')
test.square_track()
print('ellipse_square (мм)', test.ellipse_square)
"""
