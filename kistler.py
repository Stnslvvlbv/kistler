from read_file import readFile
from moving_average import moving_average
from paint_track import paint
from klaster import klasters_array
from total_way import total_way, average
from ewma import ewma
from standart_deviation import stand_dev


class kistler():
    def __init__(self, url):
        self.url = url
        self.freshData = readFile(url)
        self.total_way = total_way(self.freshData)
        self.average = average(self.total_way)
        self.standart_deviation = stand_dev(self.freshData, self.total_way)


    def paint_ewma(self, alpha=0.01, order_ema=1, corner_step=10):
        self.ewma = ewma(self.freshData, alpha=alpha, order_ema=order_ema)
        paint(self.ewma, corner_step=corner_step)

    def paint_moving_average(self, n=200, corner_step=10):
        self.MAarray = moving_average(self.freshData, n=n)
        paint(self.MAarray, corner_step=corner_step)

    def klaster_data(self, n=100, step=1, corner_step=10):
        self.KlasterArray = klasters_array(self.freshData, n=n, step=step)
        paint(self.KlasterArray, shift=0, corner_step=corner_step)


test = kistler('example/KseniaT 005.txt')
print(test.total_way)
print(test.average)
print(test.standart_deviation)
# test.paint_moving_average(n=400, corner_step=5)
test.paint_ewma(alpha=0.01, order_ema=3, corner_step=1)
# test.klaster_data(n=200, step=10)