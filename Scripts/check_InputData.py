import datetime


def Check_Date(date):  # Проверка даты на корректность
    try:
        datetime.datetime.strptime(date, '%d.%m.%Y')
        return True
    except ValueError:
        return False


def Check_Lesson(lesson):  # Проверка имени урока на корректность
    if len(lesson) <= 32:
        return True
    else:
        return False


def Check_Tasks(task):  # Проверка задания на корректность
    if len(task) <= 512:
        return True
    else:
        return False
