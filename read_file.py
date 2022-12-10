import os
import  numpy as np


def readFile(file_name):
    data = []
    with open(file_name, 'r') as text:
        file =file_name.split('/')[-1]
        print(f'Чтение файла, {file} извлечение данных')
        START_ROW_DATA = 19
        row = 0
        FLAG = 'start'
        while True:
            line = text.readline()
            if line[0:8] == '0.000000':
                FLAG = 'read data'
            elif len(line) < 1:
                FLAG = 'end'

            if FLAG == 'read data':
                data_row = line.strip().split('	')
                data_float =[]
                for elIndex in range(0, len(data_row)):
                    el = float(data_row[elIndex]) * 1000 # мм
                    if elIndex in [0, 17, 18]:
                        data_float.append(el)

                data.append(data_float)
            elif FLAG == 'end':
                return data

    return data
