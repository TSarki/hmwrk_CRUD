import psycopg2

def create_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
    id SERIAL PRIMARY KEY, 
    client_name VARCHAR(25) NOT NULL, 
    client_surname VARCHAR(25) NOT NULL, 
    client_email VARCHAR(30) NOT NULL
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonenumbers(
    id_number SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients(id),
    client_phonenumber VARCHAR(20) UNIQUE);
    """)
    
def add_client(cur, client_name, client_surname, client_email):
    cur.execute("""
    INSERT INTO clients(client_name, client_surname, client_email) VALUES(%s, %s, %s);
    """, (client_name, client_surname, client_email))
    
def add_new_phonenumber(cur, client_id, phonenumber):
    cur.execute("""
    INSERT INTO phonenumbers(client_id, client_phonenumber) VALUES(%s, %s);
    """, (client_id, phonenumber))
    
def change_client_data():
    print("Введите команду.\n "
    "change name - изменить имя; change surname - изменить фамилию; change mail - изменить e-mail; change number - изменить номер телефона")

    while True:
        command_symbol = input()
        if command_symbol == 'change name':
            changing_name_id = input("Введите id клиента имя которого хотите изменить: ")
            new_name = input("Введите новое имя: ")
            cur.execute("""
            UPDATE clients SET client_name=%s WHERE id=%s;
            """, (new_name, changing_name_id))
            break
        elif command_symbol == 'change surname':
            changing_surname_id = input("Введите id клиента фамилию которого хотите изменить: ")
            new_surname = input("Введите новую фамилию: ")
            cur.execute("""
            UPDATE clients SET client_surname=%s WHERE id=%s;
            """, (new_surname, changing_surname_id))
            break
        elif command_symbol == 'change mail':
            changing_mail_id = input("Введите id клиента e-mail которого хотите изменить: ")
            new_mail = input("Введите новый e-mail: ")
            cur.execute("""
            UPDATE clients SET client_email=%s WHERE id=%s;
            """, (new_mail, changing_mail_id))
            break
        elif command_symbol == 'change number':
            phonenumber_to_change = input("Введите номер телефона который Вы хотите изменить: ")
            new_phonenumber = input("Введите новый номер телефона: ")
            cur.execute("""
            UPDATE phonenumbers SET client_phonenumber=%s WHERE client_phonenumber=%s;
            """, (new_phonenumber, phonenumber_to_change))
            break
        else:
            print("Команда отсутствует, повторите ввод")
            
def delete_phonenumber():
    client_id_to_delete_phonenumber = input("Введите id клиента номер телефона которого хотите удалить: ")
    phonenumber_for_deleting = input("Введите номер телефона который хотите удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phonenumbers WHERE client_id=%s AND client_phonenumber=%s
        """, (client_id_to_delete_phonenumber, phonenumber_for_deleting))
        
def delete_client():
    input_id = input("Введите id клиента которого хотите удалить: ")
    input_client_surname = input("Введите фамилию клиента которого хотите удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phonenumbers WHERE client_id=%s
        """, (input_id,))
        cur.execute("""
        DELETE FROM clients WHERE id=%s AND client_surname=%s
        """, (input_id, input_client_surname))
        
def search_client():
    print("Для поиска информации о клиенте, пожалуйста, введите команду, где:\n "
          "1 - найти по имени; 2 - найти по фамилии; 3 - найти по e-mail; 4 - найти по номеру телефона")
    while True:
        input_command = int(input("Введите команду для поиска информации о клиенте: "))
        if input_command == 1:
            search_by_name = input("Введите имя для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, client_name, client_surname, client_email, client_phonenumber
            FROM clients AS c
            LEFT JOIN client_phonenumbers AS cp ON cp.id_phonenumber = c.id
            WHERE client_name=%s
            """, (search_by_name,))
            print(cur.fetchall())
        elif input_command == 2:
            search_by_surname = input("Введите фамилию для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, client_name, client_surname, client_email, client_phonenumber
            FROM clients AS c
            LEFT JOIN phonenumbers AS cp ON cp.id_phonenumber = c.id
            WHERE client_surname=%s
            """, (search_by_surname,))
            print(cur.fetchall())
        elif input_command == 3:
            search_by_email = input("Введите email для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, client_name, client_surname, client_email, client_phonenumber
            FROM clients AS c
            LEFT JOIN phonenumbers AS cp ON cp.id_phonenumber = c.id
            WHERE client_email=%s
            """, (search_by_email,))
            print(cur.fetchall())
        elif input_command == 4:
            search_by_phonenumber = input("Введите номер телефона для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, client_name, client_surname, client_email, client_phonenumber
            FROM clients AS c
            LEFT JOIN phonenumbers AS cp ON cp.id_phonenumber = c.id
            WHERE client_phonenumber=%s
            """, (search_by_phonenumber,))
            #return cur.fetchone()[0]
            print(cur.fetchall())
        else:
            print("Команда отсутствует, повторите ввод")

with psycopg2.connect(user="postgres", password="ds76TRmn", database="hmwrk_clients") as conn:
    with conn.cursor() as cur:
        create_db(cur)
        add_client(cur, "Harry", "Potter", "hp@mail.com")
        add_client(cur, "Tony", "Stark", "ts@mail.com")
        add_client(cur, "Ryan", "Gosling", "rg@mail.com")
        add_client(cur, "Tom", "Ford", "tf@mail.com")
        add_client(cur, "Charley", "Parker", "cp@mail.com")
        add_new_phonenumber(cur, 1, "1111")
        add_new_phonenumber(cur, 2, "2222")
        add_new_phonenumber(cur, 3, "3333")
        add_new_phonenumber(cur, 4, "4444")
        add_new_phonenumber(cur, 5, "5555")
        change_client_data()
        delete_phonenumber()
        delete_client()
        search_client()