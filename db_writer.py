import psycopg2
import pandas as pd
import pandas.io.sql as sqlio
from psycopg2 import Error
from db_readfile import read_folder_name, find_txt_file, extract_data_from_txt
from read_file import readFile

def start_session(func):

    def wrapper(*args, **kwargs):
        try:
            # Подключиться к существующей базе данных
            connection = psycopg2.connect(user="postgres",
                                          # пароль, который указали при установке PostgreSQL
                                          password="1111",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="kistler")
            cursor = connection.cursor()

            result = None
            result = func(cursor=cursor, connection=connection, *args, **kwargs)


        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

        return result
    return wrapper

@start_session
def db_create_table_fresh_data(cursor, connection):
    create_table_query = '''CREATE TABLE fresh_data
                             (ID SERIAL  PRIMARY KEY,
                             TEST_SUBJECT    integer   REFERENCES test_subject(ID)   NOT NULL,
                             RECORD_TYPE           VARCHAR(64)    NOT NULL,
                             RECORD_NUMBER           integer    NOT NULL,
                             abs_time_s    NUMERIC(6, 3)      ARRAY,
                             Fx     NUMERIC(9, 6)      ARRAY,
                             Fy     NUMERIC(9, 6)      ARRAY,
                             Fz     NUMERIC(10, 6)      ARRAY,
                             Ft     NUMERIC(10, 6)      ARRAY,
                             Ax     NUMERIC(7, 6)      ARRAY,
                             Ay    NUMERIC(7, 6)      ARRAY); '''
    create_table_query1 = '''CREATE TABLE test_subject
                                 (ID SERIAL  PRIMARY KEY,
                                 TEST_SUBJECT           VARCHAR(64)    NOT NULL); '''

    cursor.execute(create_table_query)
    connection.commit()
    print("Таблица успешно создана в PostgreSQL")


@start_session
def db_write_test_subject(cursor, connection, folder):
    list_subject = read_folder_name(folder)
    print(list_subject)

    # pk = 0
    cursor.execute('SELECT * FROM test_subject')
    data = cursor.fetchall()
    db_list_subject = []
    for el in data:
        db_list_subject.append(el[1])
        # pk = el[0]

    for el in list_subject:

        if el not in db_list_subject:

            # pk += 1
            cursor.execute('INSERT INTO test_subject (TEST_SUBJECT) VALUES (%s)', (el,))
            connection.commit()
            print("испытуемый", el, "добавлен в базу")
        else:
            print('запись', el, "уже существует")
    print(el)

@start_session
def subject_request(cursor, connection, folder):
    list_subject = read_folder_name(folder)

    cursor.execute('SELECT * FROM test_subject')
    data = cursor.fetchall()

    for el in data:

        if not el[1] in list_subject:
            print("В базе данных присутствует испытуемый", el[1], "но отсутствует в дериктории импорта")
            answer = input('Для остановки записи базы данных введите "stop", для записи без испытуемого "next": \n')
            if answer == 'stop':
                break
            elif answer == 'next':
                data.remove(el)

    return data


@start_session
def write_element_fresh_data(cursor, connection, data_element):
    cursor.execute('''INSERT INTO fresh_data 
        (TEST_SUBJECT, RECORD_TYPE, RECORD_NUMBER, abs_time_s, Fx, Fy, Fz, Ft, Ax, Ay) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                   (data_element['foreign_key'], data_element['record_type'], data_element['record_number'],
                    data_element['abs time (s)'], data_element['Fx'], data_element['Fy'],
                    data_element['Fz'], data_element['|Ft|'], data_element['Ax'],
                    data_element['Ay'])
                   )
    connection.commit()
    print("данные записанны")

def db_write_fresh_data(folder):
    # проверка на наличие новых испытуемых
    print("запись не обработанных данных в базу")
    list_subject = read_folder_name(folder)

    data = subject_request(folder=folder)

    for el in data:
        record_folder = folder + '/' + el[1]
        record_list = find_txt_file(record_folder)

        for txt in record_list:
            data_element = extract_data_from_txt(record_folder + '/' + txt)
            data_element['foreign_key'] = el[0]
            print("запись данных из файла", txt)
            write_element_fresh_data(data_element=data_element)


@start_session
def get_primary_key(cursor, connection, columns, table):
    select = 'SELECT ' + columns + ' FROM ' + table
    cursor.execute(select)
    result = cursor.fetchall()

    return result


@start_session
def get_object_by_value(cursor, connection, columns, table, element_filter, value):
    select = 'SELECT ' + columns + ' FROM ' + table + ' WHERE ' + element_filter + ' = ' + str(value)

    cursor.execute(select)
    result = cursor.fetchone()

    return result


def analysis_data():
    # list_id_fresh_data = get_primary_key(columns='id', table='fresh_data')
    object_data = get_object_by_value(columns='ID, TEST_SUBJECT, RECORD_TYPE, RECORD_NUMBER, abs_time_s, Ax, Ay ', table='fresh_data', element_filter='id', value=1)
    object_data_dict = {}

    object_data_dict = {
        'abs_time_s': list(map(lambda x: float(x), object_data[4])),
        'Ax': list(map(lambda x: float(x), object_data[5])),
        'Ay': list(map(lambda x: float(x), object_data[6])),
    }
    dataPD = pd.DataFrame.from_dict(object_data_dict)
    """ (ID SERIAL  PRIMARY KEY,
                             TEST_SUBJECT    integer   REFERENCES test_subject(ID)   NOT NULL,
                             RECORD_TYPE           VARCHAR(64)    NOT NULL,
                             RECORD_NUMBER           integer    NOT NULL,
                             abs_time_s    NUMERIC(6, 3)      ARRAY,
                             Fx     NUMERIC(9, 6)      ARRAY,
                             Fy     NUMERIC(9, 6)      ARRAY,
                             Fz     NUMERIC(10, 6)      ARRAY,
                             Ft     NUMERIC(10, 6)      ARRAY,
                             Ax     NUMERIC(7, 6)      ARRAY,
                             Ay    NUMERIC(7, 6)      ARRAY);"""

    """for col in object_data[4:]:
        el_list = list(map(lambda x: float(x), col))
        object_data_list.append(el_list)"""
    print(dataPD)


analysis_data()

# db_create_table_fresh_data()
# db_write_test_subject(folder='D:/pr/kistler/data/Stabila_records')
# db_write_fresh_data(folder='D:/pr/kistler/data/Stabila_records')


