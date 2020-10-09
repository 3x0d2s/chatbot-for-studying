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

    def get_admins(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM `admins`")
            return self.cursor.fetchall()

    def add_Homework(self, date, weekDay, lesson, task):
        with self.connection:
            return self.cursor.execute("INSERT INTO `homework` (`compl_date`, 'weekday', 'lesson', 'task') VALUES(?,?,?,?)", (date, weekDay, lesson, task))

    def delete_payment(self, user_id):
        with self.connection:
            self.cursor.execute(
                "DELETE FROM `payments` WHERE `user_id` = ?", (user_id,))

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
