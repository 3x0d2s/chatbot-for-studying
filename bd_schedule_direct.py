import sqlite3

class scheduleDirect:
    rowcount = 0
    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_Lesson(self, id_lesson):
        with self.connection:
            #self.cursor.execute("SELECT * FROM `schedule_saturday` WHERE `id_lesson` = ?", (str(id_lesson),))
            self.cursor.execute("SELECT * FROM `schedule_saturday`")
            rowcount = self.cursor.rowcount
            return self.cursor.fetchall()

    def add_paymentToStack(self, user_id, code):
        """Добавляем"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `payments` (`user_id`, 'code') VALUES(?,?)", (user_id, code))

    def delete_payment(self, user_id):
        with self.connection:
            self.cursor.execute("DELETE FROM `payments` WHERE `user_id` = ?", (user_id,))

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()