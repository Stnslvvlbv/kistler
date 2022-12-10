import numpy as np

from read_file import readFile

CONST_A = 0.21
CONST_B = 0.26
CONST_AZ0 = - 0.041
def test_values(data):
    self_count = []
    dataNp = np.array(data)
    dataNpTransponse = dataNp.transpose()
    self_count.append(dataNpTransponse[0])
    array_Fx12 = dataNpTransponse[5]
    array_Fx34 = dataNpTransponse[6]
    array_Fy14 = dataNpTransponse[7]
    array_Fy23 = dataNpTransponse[8]
    array_Fz1 = dataNpTransponse[9]
    array_Fz2 = dataNpTransponse[10]
    array_Fz3 = dataNpTransponse[11]
    array_Fz4 = dataNpTransponse[12]

    array_Fx = array_Fx12 + array_Fx34
    self_count.append(array_Fx)

    array_Fy = array_Fy14 + array_Fy23
    self_count.append(array_Fy)

    array_Fz = array_Fz1 + array_Fz2 + array_Fz3 + array_Fz4
    self_count.append(array_Fz)

    array_Mx = CONST_B * (array_Fz1 + array_Fz2 - array_Fz3 - array_Fz4)
    array_Mx_ = CONST_B * (array_Fz1 + array_Fz2 - array_Fz3 - array_Fz4) + ан

    printArray =array_Mx #больше на 5,12 % экспортированных данных
    print(printArray, len(printArray))

data = readFile('D:\pr\kistler\example\export\Evgeniy_auto_center\Evgeniy 001.txt')
test_values(data)