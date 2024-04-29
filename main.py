import psycopg2
import random
from datetime import datetime, timedelta


class TaxiApp:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="taxi",
            user="postgres",
            password="postgres",
            host="localhost"
        )
        self.cursor = self.conn.cursor()

    def get_random_client(self):
        self.cursor.execute("SELECT * FROM clients ORDER BY RANDOM() LIMIT 1")
        return self.cursor.fetchone()

    def get_random_driver(self):
        self.cursor.execute("SELECT * FROM drivers ORDER BY RANDOM() LIMIT 1")
        return self.cursor.fetchone()

    def create_ride(self, client_id, driver_id):
        destination = "Random destination"  # Место назначения может быть генерируемым
        payment_method = random.choice(["cash", "card"])
        estimated_arrival_time = datetime.now() + timedelta(minutes=random.randint(5, 30))

        self.cursor.execute("""
            INSERT INTO rides (driver_id, client_id, destination, payment_method, estimated_arrival_time)
            VALUES (%s, %s, %s, %s, %s)
        """, (driver_id, client_id, destination, payment_method, estimated_arrival_time))
        self.conn.commit()

    @staticmethod
    def show_main_menu():
        print("Меню:")
        print("1. Я таксист")
        print("2. Я клиент")
        print("3. Выход")

    @staticmethod
    def show_driver_menu():
        print("1. Выйти на смену")
        print("2. Назад")

    @staticmethod
    def show_client_menu():
        print("1. Заказать такси")
        print("2. Назад")

    @staticmethod
    def show_driver_accept_menu():
        print("1. Принять поездку")
        print("2. Отказаться")
        print("3. Назад")

    @staticmethod
    def show_client_accept_menu():
        print("1. Принять водителя")
        print("2. Отказаться")
        print("3. Назад")

    def run(self):
        while True:
            self.show_main_menu()
            choice = input("Выберите опцию: ")

            if choice == '1':  # Я таксист
                while True:
                    self.show_driver_menu()
                    driver_choice = input("Выберите опцию: ")

                    if driver_choice == '1':  # Выйти на смену
                        client = self.get_random_client()
                        print("Информация о клиенте:")
                        print(f"Имя: {client[1]}")
                        print(f"Рейтинг: {client[2]}")
                        print(f"Способ оплаты: {random.choice(['cash', 'card'])}")
                        print(f"Место назначения: Random destination")
                        print(f"Время поездки: {random.randint(5, 30)} минут")

                        self.show_driver_accept_menu()
                        accept_choice = input("Выберите опцию: ")

                        if accept_choice == '1':  # Принять поездку
                            self.create_ride(client[0], 1)
                            print("Поездка закончилась! Всего хорошего!")
                            break
                        elif accept_choice == '2':  # Отказаться
                            continue
                        elif accept_choice == '3':  # Назад
                            break
                        else:
                            print("Неверный выбор.")

                    elif driver_choice == '2':  # Назад
                        break
                    else:
                        print("Неверный выбор.")

            elif choice == '2':  # Я клиент
                while True:
                    self.show_client_menu()
                    client_choice = input("Выберите опцию: ")

                    if client_choice == '1':  # Заказать такси
                        driver = self.get_random_driver()
                        print("Информация о водителе:")
                        print(f"Имя: {driver[1]}")
                        print(f"Рейтинг: {driver[2]}")
                        print(f"Время прибытия: {random.randint(5, 15)} минут")

                        self.show_client_accept_menu()
                        accept_choice = input("Выберите опцию: ")

                        if accept_choice == '1':  # Принять водителя
                            print("Поездка закончилась! Всего хорошего!")
                            break
                        elif accept_choice == '2':  # Отказаться
                            continue
                        elif accept_choice == '3':  # Назад
                            break
                        else:
                            print("Неверный выбор.")

                    elif client_choice == '2':  # Назад
                        break
                    else:
                        print("Неверный выбор.")

            elif choice == '3':  # Выход
                print('Всего доброго!')
                break
            else:
                print("Неверный выбор.")


if __name__ == "__main__":
    app = TaxiApp()
    app.run()
