import os


def readTXT(file_name):
    data = []
    with open(file_name, 'r') as text:
        file =file_name.split('/')[-1]
        print(f'Чтение файла, {file} извлечение данных')
        START_ROW_DATA = 19
        row = 0
        while True:
            line = text.readline()

            if len(line) < 3:
                return data

            elif START_ROW_DATA > row:
                row += 1
            elif START_ROW_DATA == row:
                data_row = line.strip().split('	')
                data_float =[]
                for el in data_row:
                    el = float(el)
                    data_float.append(el)
                data.append(data_float)


result = readTXT('example/KseniaT 005.txt')
print(result)
