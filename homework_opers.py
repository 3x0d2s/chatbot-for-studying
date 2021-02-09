import datetime


class Homework:

    def set_Weekday(self, value=None):
        if value == None:
            idWeekday = datetime.datetime.strptime(
                self.date, '%d.%m.%Y').weekday()
            weekdays = ['Понедельник', 'Вторник', 'Среда',
                        'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
            self.weekday = weekdays[idWeekday]
        else:
            self.weekday = value
            self.get_DateByWeekday(value)

    def get_Weekday(self):
        return self.weekday

    def get_DateByWeekday(self, weekday, mode=0):
        weekdays = ['Понедельник', 'Вторник', 'Среда',
                    'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        idSecondWeekday = 0
        for w in weekdays:
            if w == weekday:
                break
            else:
                idSecondWeekday += 1
        now = datetime.datetime.now()
        idThisWeekday = now.weekday()
        #
        if idSecondWeekday <= idThisWeekday:
            delt = (6 - idThisWeekday) + idSecondWeekday
            dur_days = datetime.timedelta(days=(delt + 1))
            result = now + dur_days
            date = result.strftime('%d.%m.%Y')
            if mode == 0:
                self.set_Date(date)
            elif mode == 1:
                return date
        elif idSecondWeekday > idThisWeekday:
            delt = idSecondWeekday - idThisWeekday
            dur_days = datetime.timedelta(days=delt)
            result = now + dur_days
            date = result.strftime('%d.%m.%Y')
            if mode == 0:
                self.set_Date(date)
            elif mode == 1:
                return date

    def get_WeekdayByDate(self, date):
        # idWeekday = datetime.datetime.strptime(
        #     self.date, '%d.%m.%Y').weekday()
        idWeekday = date.weekday()
        weekdays = ['Понедельник', 'Вторник', 'Среда',
                    'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        return weekdays[idWeekday]

    def set_Date(self, Date):
        self.date = Date
        self.set_Weekday()

    def get_Date(self):
        return self.date

    def set_Lesson(self, Lesson):
        self.lesson = Lesson

    def get_Lesson(self):
        return self.lesson

    def set_Task(self, Task):
        self.task = Task

    def get_Task(self):
        return self.task

    def clear_Stack(self):
        self.date = None
        self.weekday = None
        self.lesson = None
        self.task = None
