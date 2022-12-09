from read_file import readFile
from moving_average import moving_average
from paint_track import paint
from klaster import klasters_array
from total_way import total_way, average


class kistler():
    def __init__(self, url):
        self.url = url
        self.freshData = readFile(url)
        self.total_way = total_way(self.freshData)
        self.average = average(self.total_way)
        # self.test = paint(self.MAarray)

    def paint_moving_average(self, n=200):
        self.MAarray = moving_average(self.freshData, n=n)
        paint(self.MAarray)

    def klaster_data(self, n=100, step=1):
        self.KlasterArray = klasters_array(self.freshData, n=n, step=step)
        paint(self.KlasterArray, shift=0)


test = kistler('example/KseniaT 005.txt')
print(test.total_way)
print(test.average)
# test.paint_moving_average(n=400)
# test.klaster_data(n=200, step=10)