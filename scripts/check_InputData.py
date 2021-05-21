import datetime


def Check_Date(date):
    """Проверяет дату на корректность."""
    try:
        datetime.datetime.strptime(date, '%d.%m.%Y')
        return True
    except ValueError:
        return False


def Check_Lesson(lesson):  # Проверка имени урока на корректность
    """Проверяет имя урока на длину."""
    if len(lesson) <= 32:
        return True
    else:
        return False


def Check_Tasks(task):
    """Проверяет задание на длину."""
    if len(task) <= 512:
        return True
    else:
        return False
