import sqlite3


def createBD_FromDump():
    cur = sqlite3.connect("/db/db.db")
    f = open('Data Base/db_dump.sql', 'r')
    dump = f.read()
    cur.executescript(dump)


class requestDB:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def getUserHomewFlag(self, user_id):
        with self.connection:
            self.cursor.execute(
                "SELECT homework_f FROM users WHERE user_id=?", (user_id,))
            return (self.cursor.fetchall())[0][0]

    def getUserSchedFlag(self, user_id):
        with self.connection:
            self.cursor.execute(
                "SELECT schedule_f FROM users WHERE user_id=?", (user_id,))
            return (self.cursor.fetchall())[0][0]

    def getUserAddHomewFlag(self, user_id):
        with self.connection:
            self.cursor.execute(
                "SELECT addHomew_f FROM users WHERE user_id=?", (user_id,))
            return (self.cursor.fetchall())[0][0]

    def getUserDelHomewFlag(self, user_id):
        with self.connection:
            self.cursor.execute(
                "SELECT delHome_f FROM users WHERE user_id=?", (user_id,))
            return (self.cursor.fetchall())[0][0]

    def getUserGetLessDateFlag(self, user_id):
        with self.connection:
            self.cursor.execute(
                "SELECT getLessDate_f FROM users WHERE user_id=?", (user_id,))
            return (self.cursor.fetchall())[0][0]

    def getUserStepCode(self, user_id):
        with self.connection:
            self.cursor.execute(
                "SELECT step_code FROM users WHERE user_id=?", (user_id,))
            return (self.cursor.fetchall())[0][0]

    def getUserEditHomewFlag(self, user_id):
        with self.connection:
            self.cursor.execute(
                "SELECT editHomew_f FROM users WHERE user_id=?", (user_id,))
            return (self.cursor.fetchall())[0][0]

    def changeUserHomewFlag(self, user_id, value):
        with self.connection:
            return self.cursor.execute(
                "UPDATE users SET homework_f=? WHERE user_id=?", (value, user_id))

    def changeUserSchedFlag(self, user_id, value):
        with self.connection:
            return self.cursor.execute(
                "UPDATE users SET schedule_f=? WHERE user_id=?", (value, user_id))

    def changeUserAddHomewFlag(self, user_id, value):
        with self.connection:
            return self.cursor.execute(
                "UPDATE users SET addHomew_f=? WHERE user_id=?", (value, user_id))

    def changeUserDelHomewFlag(self, user_id, value):
        with self.connection:
            return self.cursor.execute(
                "UPDATE users SET delHome_f=? WHERE user_id=?", (value, user_id))

    def changeUserGetLessDateFlag(self, user_id, value):
        with self.connection:
            return self.cursor.execute(
                "UPDATE users SET getLessDate_f=? WHERE user_id=?", (value, user_id))

    def changeUserStepCode(self, user_id, value):
        with self.connection:
            return self.cursor.execute(
                "UPDATE users SET step_code=? WHERE user_id=?", (value, user_id))

    def changeUserEditHomewFlag(self, user_id, value):
        with self.connection:
            return self.cursor.execute(
                "UPDATE users SET editHomew_f=? WHERE user_id=?", (value, user_id))

    def get_Lesson(self, weekday, weekConfig):
        with self.connection:
            if weekConfig == '1':
                self.cursor.execute(
                    "SELECT * FROM `schedule_1` WHERE weekday IN (?)", (weekday, ))
            elif weekConfig == '2':
                self.cursor.execute(
                    "SELECT * FROM `schedule_2` WHERE weekday IN (?)", (weekday, ))
            return self.cursor.fetchall()

    def get_Homework(self, date):
        with self.connection:
            self.cursor.execute(
                "SELECT lesson, task FROM `homework` WHERE compl_date IN (?)", (date, ))
            return self.cursor.fetchall()

    def get_allHomework(self):
        with self.connection:
            self.cursor.execute(
                "SELECT compl_date, lesson, task FROM `homework`")
            return self.cursor.fetchall()

    def editTaskForHomework(self, date, lesson, task):
        with self.connection:
            return self.cursor.execute(
                "UPDATE homework SET task=? WHERE compl_date=? AND lesson=?", (task, date, lesson))

    def editDateForHomework(self, old_date, lesson, new_date):
        with self.connection:
            return self.cursor.execute(
                "UPDATE homework SET compl_date=? WHERE compl_date=? AND lesson=?", (new_date, old_date, lesson))

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES(?) ", (user_id,))

    def get_users(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM `users`")
            return self.cursor.fetchall()

    def add_HomeworkObjectToStack(self, user_id, date, weekDay, lesson, task):  # STACK
        with self.connection:
            return self.cursor.execute("INSERT INTO `homework_stack` (`user_id`, `compl_date`, 'weekday', 'lesson', 'task') VALUES(?,?,?,?,?)", (user_id, date, weekDay, lesson, task))

    def HomeworkStack_setDate(self, user_id, value):
        with self.connection:
            return self.cursor.execute(
                "UPDATE homework_stack SET compl_date=? WHERE user_id=?", (value, user_id))

    def HomeworkStack_setWeekday(self, user_id, value):
        with self.connection:
            return self.cursor.execute(
                "UPDATE homework_stack SET weekday=? WHERE user_id=?", (value, user_id))

    def HomeworkStack_setLesson(self, user_id, value):
        with self.connection:
            return self.cursor.execute(
                "UPDATE homework_stack SET lesson=? WHERE user_id=?", (value, user_id))

    def HomeworkStack_setTask(self, user_id, value):
        with self.connection:
            return self.cursor.execute(
                "UPDATE homework_stack SET task=? WHERE user_id=?", (value, user_id))

    def HomeworkStack_getDate(self, user_id):
        with self.connection:
            self.cursor.execute(
                "SELECT compl_date FROM homework_stack WHERE user_id=?", (user_id,))
            return (self.cursor.fetchall())[0][0]

    def HomeworkStack_getWeekday(self, user_id):
        with self.connection:
            self.cursor.execute(
                "SELECT weekday FROM homework_stack WHERE user_id=?", (user_id,))
            return (self.cursor.fetchall())[0][0]

    def HomeworkStack_getLesson(self, user_id):
        with self.connection:
            self.cursor.execute(
                "SELECT lesson FROM homework_stack WHERE user_id=?", (user_id,))
            return (self.cursor.fetchall())[0][0]

    def HomeworkStack_getTask(self, user_id):
        with self.connection:
            self.cursor.execute(
                "SELECT task FROM homework_stack WHERE user_id=?", (user_id,))
            return (self.cursor.fetchall())[0][0]

    def del_HomeworkObjectFromStack(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `homework_stack` WHERE user_id=?", (user_id,))

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
