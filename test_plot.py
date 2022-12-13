import os

def iter_file(folder):
    files = os.listdir(folder)
    image_folder = folder + '/' + 'images'
    if os.path.exists(image_folder) == False:
        os.mkdir(image_folder)

    for filename in files:
        print(filename)
        url = folder + '/' + filename


iter_file('D:/pr/kistler/example/auto_center')


