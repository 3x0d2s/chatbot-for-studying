import sqlite3


class bdDirect:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_Lesson(self, weekday):
        with self.connection:
            self.cursor.execute(
                "SELECT * FROM `schedule` WHERE weekday IN (?)", (weekday, ))
            return self.cursor.fetchall()

    def get_Homework(self, date):
        with self.connection:
            self.cursor.execute(
                "SELECT lesson, task FROM `homework` WHERE compl_date IN (?)", (date, ))
            return self.cursor.fetchall()

    def get_allHomework(self):
        with self.connection:
            self.cursor.execute(
                "SELECT compl_date, lesson FROM `homework`")
            return self.cursor.fetchall()

    def get_admins(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM `admins`")
            return self.cursor.fetchall()

    def add_Homework(self, date, weekDay, lesson, task):
        with self.connection:
            return self.cursor.execute("INSERT INTO `homework` (`compl_date`, 'weekday', 'lesson', 'task') VALUES(?,?,?,?)", (date, weekDay, lesson, task))

    def del_Homework(self, date, lesson):
        with self.connection:
            return self.cursor.execute("DELETE FROM `homework` WHERE compl_date=? AND lesson=?", (date, lesson))

    def check_Homework(self, date, lesson):
        with self.connection:
            homework = self.cursor.execute(
                "SELECT * FROM `homework` WHERE compl_date=? AND lesson=?", (date, lesson))
            if len(homework.fetchall()) != 0:
                return True
            else:
                return False

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
