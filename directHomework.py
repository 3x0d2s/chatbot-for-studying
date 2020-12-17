import datetime


class Homework:

    def Set_Weekday(self, value=None):
        if value == None:
            idWeekday = datetime.datetime.strptime(
                self.date, '%d.%m.%Y').weekday()
            weekdays = ['Понедельник', 'Вторник', 'Среда',
                        'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
            self.weekday = weekdays[idWeekday]
        else:
            self.weekday = value
            self.Get_DateByWeekday(value)

    def Get_Weekday(self):
        return self.weekday

    def Get_DateByWeekday(self, weekday, mode=0):
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
                self.Set_Date(date)
            elif mode == 1:
                return date
        elif idSecondWeekday > idThisWeekday:
            delt = idSecondWeekday - idThisWeekday
            dur_days = datetime.timedelta(days=delt)
            result = now + dur_days
            date = result.strftime('%d.%m.%Y')
            if mode == 0:
                self.Set_Date(date)
            elif mode == 1:
                return date

    def Set_Date(self, Date):
        self.date = Date
        self.Set_Weekday()

    def Get_Date(self):
        return self.date

    def Set_Lesson(self, Lesson):
        self.lesson = Lesson

    def Get_Lesson(self):
        return self.lesson

    def Set_Task(self, Task):
        self.task = Task

    def Get_Task(self):
        return self.task

    def Clear_Stack(self):
        self.date = None
        self.weekday = None
        self.lesson = None
        self.task = None
