from datetime import datetime


class addHomework:

    def setWeekday(self, value=0):
        if value == None:
            self.weekday = value
        else:
            idWeekday = datetime.strptime(self.date, '%d.%m.%Y').weekday()
            weekdays = ['Понедельник', 'Вторник', 'Среда',
                        'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
            self.weekday = weekdays[idWeekday]

    def getWeekday(self):
        return self.weekday

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
        self.setDate(None)
        self.setWeekday(None)
        self.setLesson(None)
        self.setTask(None)
