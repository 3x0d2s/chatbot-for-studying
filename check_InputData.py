import datetime


def check_Date(date):  # Проверка даты на корректность
    try:
        datetime.datetime.strptime(date, '%d.%m.%Y')
        return True
    except ValueError:
        return False


def check_Lesson(lesson):  # Проверка имени урока на корректность
    if len(lesson) <= 32:
        return True
    else:
        return False


def check_Tasks(task):  # Проверка имени урока на корректность
    if len(task) <= 256:
        return True
    else:
        return False
