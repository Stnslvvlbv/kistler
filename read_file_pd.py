import pandas as pd


def readFile(file_name, window):

    MILLIMETERS = 1000  # in meter
    with open(file_name, 'r') as text:
        # file =file_name.split('/')[-1]
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

    dataPD = pd.DataFrame(data,  index=None, columns=header)

    dataPD['Ax'] *= MILLIMETERS
    dataPD['Ay'] *= MILLIMETERS

    data_moving_average = dataPD.rolling(window, on='abs time (s)', min_periods=1).mean()

    return data_moving_average



# test = readFile('example/sample.txt')
# print(test)