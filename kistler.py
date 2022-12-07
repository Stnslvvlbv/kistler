from extract_data import readTXT
from moving_average import moving_average
from paint_track import paint
from klaster import klasters_array


class kistler():
    def __init__(self, url):
        self.url = url
        self.freshData = readTXT(url)
        self.MAarray = moving_average(self.freshData)
        # self.test = paint(self.MAarray)

    def paint_moving_average(self):
        paint(self.MAarray)

    def klaster_data(self):
        self.KlasterArray = klasters_array(self.freshData)
        paint(self.KlasterArray)


test = kistler('example/KseniaT 005.txt')
test.paint_moving_average()
test.klaster_data()