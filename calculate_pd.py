import pandas as pd
from math import sqrt, pi, cos, radians
import math

def total_way(dataPD):
    STEP = 10
    wayX = 0
    wayY = 0
    total = 0

    for IndexEl in range(1, len(dataPD)):

        deltaX = abs(dataPD['Ax'][IndexEl] - dataPD['Ax'][IndexEl-1])
        deltaY = abs(dataPD['Ay'][IndexEl] - dataPD['Ay'][IndexEl-1])

        wayX += deltaX
        wayY += deltaY

        way_element = sqrt(deltaX ** 2 + deltaY ** 2)
        total += way_element

    return {'wayX (мм)': round(wayX, 2), 'wayY (мм)': round(wayY, 2), 'total_way (мм)': round(total, 2)}


def name_cuter(url):
    name_txt_file = url.split('/')[-1]
    name = name_txt_file.split('.')[0]
    return name


def triangle_square(x1, y1, x2, y2, x3, y3):

    a = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    b = sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)
    c = sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2)
    p = (a + b + c) / 2
    res = math.sqrt(p * (p - a) * (p - b) * (p - c))
    return res

def square(dataPD, average):
    STEP_CORNER = 3
    index = 0
    list_index = []
    for name, value in dataPD.items():
        if name in ['Ax', 'Ay']:
            list_index.append(index)
        index += 1

    trackPD = dataPD.iloc[:, list_index] # .sort_values(by=['Ax'])
    # trackPD['Ax'] -= average['averageX (мм)']
    # trackPD['Ay'] -= average['averageY (мм)']


    max_radius = {'quarter1' : {}, 'quarter2': {}, 'quarter3': {}, 'quarter4': {}}
    for el in range(0, 360, STEP_CORNER):
        label = str(el) + '-' + str(el + STEP_CORNER)
        min = round(math.cos(radians(el)), 6)
        max = round(math.cos(radians(el + STEP_CORNER)), 6)
        segment =  {'segment': [min, max], 'max': 0, 'row': [],}
        if 0 <= el < 90:
            max_radius['quarter1'][label] = segment
        elif 90 <= el < 180:
            max_radius['quarter2'][label] = segment
        elif 180 <= el < 270:
            max_radius['quarter3'][label] = segment
        elif 270 <= el < 360:
            max_radius['quarter4'][label] = segment

    for i, row in trackPD.iterrows():
        row['Ax'] -= average['averageX (мм)']
        row['Ay'] -= average['averageY (мм)']
        radius = sqrt(row['Ax'] ** 2 + row['Ay'] ** 2)
        cos = (row['Ax'] / radius)

        '''поиск максимально отдаленных точек по сегментам'''
        if row['Ax'] >= 0 and row['Ay'] > 0:  # первая четверть
            for key in max_radius['quarter1']:
                el = max_radius['quarter1'][key]
                if el['segment'][1] <= cos < el['segment'][0]:
                    if radius > el['max']:
                        el['max'] = radius
                        el['row'] = [
                            row['Ax'] + average['averageX (мм)'],
                            row['Ay'] + average['averageY (мм)'],
                        ]

        elif row['Ax'] <= 0 and row['Ay'] > 0: # вторая четверть
            for key in max_radius['quarter2']:
                el = max_radius['quarter2'][key]
                if el['segment'][1] <= cos < el['segment'][0]:
                    if radius > el['max']:
                        el['max'] = radius
                        el['row'] = [
                            row['Ax'] + average['averageX (мм)'],
                            row['Ay'] + average['averageY (мм)'],
                        ]

        elif row['Ax'] < 0 and row['Ay'] <= 0:  # третья четверть
            for key in max_radius['quarter3']:
                el = max_radius['quarter3'][key]
                if el['segment'][0] <= cos < el['segment'][1]:
                    if radius > el['max']:
                        el['max'] = radius
                        el['row'] = [
                            row['Ax'] + average['averageX (мм)'],
                            row['Ay'] + average['averageY (мм)'],
                        ]

        elif row['Ax'] > 0 and row['Ay'] <= 0:    #  четвертая четверть
            for key in max_radius['quarter4']:
                el = max_radius['quarter4'][key]
                if el['segment'][0] <= cos < el['segment'][1]:
                    if radius > el['max']:
                        el['max'] = radius
                        el['row'] = [
                            row['Ax'] + average['averageX (мм)'],
                            row['Ay'] + average['averageY (мм)'],
                        ]


    result_points = []
    for qr in max_radius:
        for seg in max_radius[qr]:
            result_points.append(max_radius[qr][seg]['row'])
    square_result = 0
    data_sq = pd.DataFrame(result_points, index=None, columns=['Ax', 'Ay'])

    for iter in range(0, len(result_points)):
        point2 = result_points[iter]
        if iter == 0:
            point3 = result_points[len(result_points) - 1]
        else:
            point3 = result_points[iter - 1]

        s_triangle = triangle_square(
            average['averageX (мм)'],
            average['averageY (мм)'],
            point2[0],
            point2[1],
            point3[0],
            point3[1]
        )
        square_result += s_triangle

    return {'square': square_result, 'square_points': data_sq}