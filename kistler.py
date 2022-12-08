from extract_data import readTXT
from moving_average import moving_average
from paint_track import paint
from klaster import klasters_array


class kistler():
    def __init__(self, url):
        self.url = url
        self.freshData = readTXT(url)
        # self.test = paint(self.MAarray)

    def paint_moving_average(self):
        self.MAarray = moving_average(self.freshData, n=200)
        paint(self.MAarray)

    def klaster_data(self):
        self.KlasterArray = klasters_array(self.freshData, n=100, step=1)
        paint(self.KlasterArray, shift=0)


test = kistler('example/KseniaT 005.txt')

test.klaster_data()