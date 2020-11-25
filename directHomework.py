import datetime


class Homework:

    def setWeekday(self, value=None):
        if value == None:
            idWeekday = datetime.datetime.strptime(
                self.date, '%d.%m.%Y').weekday()
            weekdays = ['Понедельник', 'Вторник', 'Среда',
                        'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
            self.weekday = weekdays[idWeekday]
        else:
            self.weekday = value
            self.getDateByWeekday(value)

    def getWeekday(self):
        return self.weekday

    def getDateByWeekday(self, weekday, mode=0):
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
                self.setDate(date)
            elif mode == 1:
                return date
        elif idSecondWeekday > idThisWeekday:
            delt = idSecondWeekday - idThisWeekday
            dur_days = datetime.timedelta(days=delt)
            result = now + dur_days
            date = result.strftime('%d.%m.%Y')
            if mode == 0:
                self.setDate(date)
            elif mode == 1:
                return date

    def setDate(self, Date):
        self.date = Date
        self.setWeekday()

    def getDate(self):
        return self.date

    def setLesson(self, Lesson):
        self.lesson = Lesson

    def getLesson(self):
        return self.lesson

    def setTask(self, Task):
        self.task = Task

    def getTask(self):
        return self.task

    def clearStack(self):
        self.date = None
        self.weekday = None
        self.lesson = None
        self.task = None
