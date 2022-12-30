import os
import pandas as pd
from read_file import readFile

# general_folder = 'D:/pr/kistler/data/Stabila_records'
def read_folder_name(folder):
    test_subject = os.listdir(folder)
    return test_subject


def find_txt_file(folder):
    test_list = os.listdir(folder)
    txt_list = []
    for el in test_list:
        if el.split('.')[-1] == 'txt':
            txt_list.append(el)
    return txt_list


def extract_data_from_txt(url):

    MILLIMETERS = 1000

    data_element = {}
    txt_name = url.split('/')[-1].split('.')[0]

    data_element['record_number'] = txt_name.split(' ')[-1]
    data_element['record_type'] = '_'.join(txt_name.split(' ')[0].split('_')[1:])

    with open(url, 'r') as text:

        FLAG = 'start'
        data = []
        while FLAG != 'end':
            line = text.readline()

            if line[0:12] == 'abs time (s)':
                FLAG = 'read header'
                header = line.strip('\n').split('\t')
            elif line[0:8] == '0.000000':
                FLAG = 'read data'
            elif len(line) < 1:
                FLAG = 'end'

            if FLAG == 'read data':
                data_row = line.strip().split('	')
                data_row_float = []
                for elIndex in range(0, len(data_row)):
                    el = float(data_row[elIndex])
                    data_row_float.append(el)
                data.append(data_row_float)

    dataPD = pd.DataFrame(data, index=None, columns=header)

    # print(dataPD['Fx'].tolist(), type(dataPD['Fx'].tolist()))
    for el in dataPD:
        data_element[el] = dataPD[el].tolist()

    return data_element
