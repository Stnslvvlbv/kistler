import os

from kistler_analizis import Kistler


def iter_file(folder):
    files = os.listdir(folder)
    image_folder = folder + '/' + 'images'
    if os.path.exists(image_folder) == False:
        os.mkdir(image_folder)

    for filename in files:
        if filename.split('.')[-1] == 'txt':
            print(filename)
            url = folder + '/' + filename

            analysis = Kistler(url)
            analysis.ellipce(image_folder)

iter_file('D:/pr/kistler/example/ST013_no_option')


