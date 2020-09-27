import sqlite3


class scheduleDirect:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_Lesson(self, weekday):
        with self.connection:
            self.cursor.execute(
                "SELECT * FROM `schedule` WHERE weekday IN (?)", (weekday, ))
            return self.cursor.fetchall()

    def get_Homework(self, weekday):
        with self.connection:
            self.cursor.execute(
                "SELECT lesson, task FROM `homework` WHERE weekday IN (?)", (weekday, ))
            return self.cursor.fetchall()

    def add_paymentToStack(self, user_id, code):
        """Добавляем"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `payments` (`user_id`, 'code') VALUES(?,?)", (user_id, code))

    def delete_payment(self, user_id):
        with self.connection:
            self.cursor.execute(
                "DELETE FROM `payments` WHERE `user_id` = ?", (user_id,))

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
