import os

from kistler_analysis import Kistler


def iter_file(folder):
    files = os.listdir(folder)
    image_folder = 'D:/pr/kistler/data/15-45sec' # folder + '/' + 'images'
    if os.path.exists(image_folder) == False:
        os.mkdir(image_folder)

    for filename in files:
        if filename.split('.')[-1] == 'txt':
            print(filename)
            url = folder + '/' + filename

            analysis = Kistler(url)
            analysis.ellipse(image_folder)

# iter_file('D:/pr/kistler/example/ST013_no_option')
list_sub = os.listdir('D:/pr/kistler/data/Stabila_records')
print(list_sub)
for el in ['ST051',]:
    folder = 'D:/pr/kistler/data/Stabila_records' + '/' + el
    print(folder)
    iter_file(folder)
