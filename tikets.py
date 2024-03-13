import sqlite3
import pandas as pd
# db = sqlite3.connect("AVIADATA.db")
# c = db.cursor()

# c.execute("""CREATE TABLE articles (
#         id INTEGER PRIMARY KEY,
#         event_name text,
#         event_date text,
#         price integer,
#         venue text,
#         tickets_available integer
# )""")

class DatabaseManager:
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

    def create(self, event_name, event_date, price, venue, tickets_available):
        add = f"INSERT INTO articles(event_name, event_date, price,venue, tickets_available) VALUES ('{event_name}', '{event_date}', {price}, '{venue}', '{tickets_available}')"
        self.cursor.execute(add)
        self.db.commit()

    def delete(self, id_del):
        self.cursor.execute(f'DELETE FROM articles WHERE "ID"={id_del}')
        self.db.commit()

    def update(self, task, id, new_value):
        if task == '1':
            query = f"Update articles set event_name='{new_value}' "
        elif task == '2':
            query =f"Update articles set event_date='{new_value}' "
        elif task == '3':
            query =f"Update articles set price={new_value} "
        elif task == '4':
            query =f"Update articles set venue={new_value} "
        elif task == '5':
            query =f"Update articles set tickets_available={new_value} "
        query = query + f' where "ID"={id}'
        self.cursor.execute(query)
        self.db.commit()

    def read(self, id):
        query = f'select * from articles where "ID"={id}'
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        for row in response:
            print(row)

    def close(self):
        self.db.close()
class Client:
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

    def read(self):
        query = 'SELECT * FROM articles'
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        for row in response:
            print(row)

    def bookable(self, id_bookable):
        query = f'SELECT tickets_available FROM articles WHERE "ID"={id_bookable}'
        self.cursor.execute(query)
        tickets_available = self.cursor.fetchone()[0]
        if tickets_available > 0:
            update_query = f'UPDATE articles SET tickets_available = tickets_available - 1 WHERE "ID"={id_bookable}'
            self.cursor.execute(update_query)
            self.db.commit()
            print("Ticket booked successfully!")
            self.save_ticket(id_bookable)
        else:
            print("Sorry, no tickets available.")

    def save_ticket(self, id_bookable):
        query = f'SELECT * FROM articles WHERE "ID"={id_bookable}'
        self.cursor.execute(query)
        ticket_data = self.cursor.fetchone()
        df = pd.DataFrame([ticket_data])
        df.to_excel(f'ticket_{id_bookable}.xlsx', index=False)
        print(f"Ticket data saved to 'ticket_{id_bookable}.xlsx'")

    def close(self):
        self.db.close()
while True:
    choices = int(input("Выберите кто использует программу \n 1)Админ \n 2)Гость , если вы гость вам не нужно вводить пароль \n 3)Выйти из сайта:"))
    if choices == 1:
        password = input('Напишите пароль Админа: ')
        if password == 'Admin':
            while True:
                db_manager = DatabaseManager("AVIADATA.db")
                choice = input('What you choice create, read, update, or Delete , exte? ')

                if choice == 'create':
                    event_name = input('Enter new event_name: ')
                    event_date = input('Enter new event_name date: ')
                    price = int(input('Enter price: '))
                    venue = input('Enter event_name venue: ')
                    tickets_available = int(input('Enter how many tickets'))
                    db_manager.create(event_name, event_date, price, venue, tickets_available)

                elif choice == 'Delete':
                    id_del = int(input('what you want to delete, give his ID ? '))
                    db_manager.delete(id_del)

                elif choice == 'update':
                    task= input('Ты будешь менять название название(1), дату(2), цену(3) или место(4) , кол-во билетов(5) ?: ')
                    id= int(input('Введи id: '))
                    new_value = input("Enter new value: ")
                    db_manager.update(task, id, new_value)

                elif choice == 'read':
                    id = int(input('Enter ID : '))
                    db_manager.read(id)
                elif choice == 'exte':
                    break

                db_manager.close()
        else:
            print("лох не правильно иди повеселись в другом месте ")
            break
    elif choices == 2:
        while True:
            cd = Client("AVIADATA.db")
            choice = input('Выбери что ты хочешь 1) Прочитать все билеты 2)Забронировать 3)Выйти ? ')
            if choice == "1":
                print("номер| название | дата | цена | место | кол-во билетов: ")
                cd.read()
            elif choice == "2":
                bronirovanie = int(input("введи номер билета нужного тебе : "))
                cd.bookable(bronirovanie)
            elif choice == "3":
                break
            else:
                print("Научись читать")
    elif choices == 3:
        break


    else :
        print('ты не правильно прочитал')
