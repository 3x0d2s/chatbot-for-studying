import datetime


def check_date(date: datetime.datetime) -> bool:
    """Проверяет дату на корректность."""
    try:
        datetime.datetime.strptime(date, '%d.%m.%Y')
        return True
    except ValueError:
        return False


def check_lesson_text(lesson: str) -> bool:
    """Проверяет имя урока на длину."""
    if len(lesson) <= 32:
        return True
    else:
        return False


def check_task_text(task: str) -> bool:
    """Проверяет задание на длину."""
    if len(task) <= 512:
        return True
    else:
        return False
