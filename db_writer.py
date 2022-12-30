import psycopg2
import pandas as pd
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
                             (ID INT PRIMARY KEY     NOT NULL,
                             TEST_SUBJECT    integer   REFERENCES test_subject(ID)   NOT NULL,
                             RECORD_TYPE           VARCHAR(64)    NOT NULL,
                             RECORD_NUMBER           integer    NOT NULL,
                             abs_time_s    NUMERIC(6, 3)      ARRAY,
                             Fx     NUMERIC(9, 6)      ARRAY,
                             Fy     NUMERIC(9, 6)      ARRAY,
                             Fz     NUMERIC(10, 6)      ARRAY,
                             Ft     NUMERIC(10, 6)      ARRAY,
                             Ax_mm     NUMERIC(6, 3)      ARRAY,
                             Ay_mm     NUMERIC(6, 3)      ARRAY); '''
    create_table_query1 = '''CREATE TABLE test_subject
                                 (ID INT PRIMARY KEY     NOT NULL,
                                 TEST_SUBJECT           VARCHAR(64)    NOT NULL); '''

    cursor.execute(create_table_query)
    connection.commit()
    print("Таблица успешно создана в PostgreSQL")


@start_session
def db_write_test_subject(cursor, connection, folder):
    list_subject = read_folder_name(folder)
    print(list_subject)

    pk = 0
    cursor.execute('SELECT * FROM test_subject')
    data = cursor.fetchall()
    db_list_subject = []
    for el in data:
        db_list_subject.append(el[1])
        pk = el[0]

    for el in list_subject:

        if el not in db_list_subject:

            pk += 1
            cursor.execute('INSERT INTO test_subject (ID, TEST_SUBJECT) VALUES (%s, %s)', (pk, el))
            connection.commit()
            print("испытуемый", el, "добавлен в базу")
        else:
            print('запись', el, "уже существует")
    print(pk)

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
            print(data_element)
    """for el in data:

        if not el[1] in list_subject:
            print("В базе данных присутствует испытуемый", el[1], "но отсутствует в дериктории импорта")
            answer = input('Для остановки записи базы данных введите "stop", для записи без испытуемого "next": \n')
            if answer == 'stop':
                break
            elif answer == 'next':
                data.remove(el)

        test_folder = folder + '/' + el[1]
        test_list = find_txt_file(test_folder)

        for txt in test_list:
            url_txt = extract_data_from_txt(test_folder + '/' + txt)

            txt_name = txt.split('.')[0]
            record_number = txt_name.split(' ')[-1]

            record_type_cute = txt_name.split(' ')[0].split('_')[1:]
            record_type = '_'.join(record_type_cute)

            dataPD = readFile(url_txt)
            print(dataPD)"""





# db_create_table_fresh_data()
db_write_fresh_data(folder='D:/pr/kistler/data/Stabila_records')