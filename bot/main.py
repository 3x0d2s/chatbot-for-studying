# -*- coding: utf8 -*-
#
import re
import os
import datetime
#
from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from loguru import logger
#
import config.config as config
from scripts.request_db import requestDB
from scripts.check_InputData import *
import scripts.config_pars
#


def show_weekdays(user_id, db):
    '''Генерирует клавиатуру из дней недели и вспомогательных кнопок.'''
    Homework_flag = db.getUserHomewFlag(user_id)
    Schedule_flag = db.getUserSchedFlag(user_id)
    addHomework_flag = db.getUserAddHomewFlag(user_id)
    #
    msg = 'Выберите...'
    #
    keyboard = VkKeyboard(one_time=False)
    if Homework_flag == True:
        keyboard.add_button('Указать число', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('На неделю', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
    if Schedule_flag == True or Homework_flag == True:
        keyboard.add_button('На сегодня', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('На завтра', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
    elif addHomework_flag == True:
        keyboard.add_button('Указать число', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('На завтра', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
    #
    keyboard.add_button('Понедельник', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Вторник', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Среда', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Четверг', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Пятница', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Суббота', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
    write_msg_withKeyboard(user_id, msg, keyboard)


def operations_with_weekdays(event, db):
    '''Функция, проводящая определенные операции при нажатии на какой-либо из дней недели.'''
    msg = event.obj.text
    addHomework_flag = db.getUserAddHomewFlag(event.obj.from_id)
    Homework_flag = db.getUserHomewFlag(event.obj.from_id)
    Schedule_flag = db.getUserSchedFlag(event.obj.from_id)
    delHomework_flag = db.getUserDelHomewFlag(event.obj.from_id)
    step_code = db.getUserStepCode(event.obj.from_id)
    #
    if Homework_flag == True:
        send_homework(event, db, msg)
        db.changeUserHomewFlag(event.obj.from_id, False)
    elif Schedule_flag == True:
        send_schedule(event, db, msg)
        db.changeUserSchedFlag(event.obj.from_id, False)
    elif addHomework_flag == True or delHomework_flag == True:
        weekday = msg
        date = get_date_by_weekday(weekday)
        db.add_HomeworkObjectToStack(event.obj.from_id, date, weekday, '', '')
        db.changeUserStepCode(event.obj.from_id, (step_code + 1))
        get_lesson(event)


def operation_today_or_tomorrow(event, db):
    '''Функция, проводящая определенные операции при нажатии на кнопки "На сегодня" и "На завтра".'''
    Schedule_flag = db.getUserSchedFlag(event.obj.from_id)
    Homework_flag = db.getUserHomewFlag(event.obj.from_id)
    addHomework_flag = db.getUserAddHomewFlag(event.obj.from_id)
    msg = event.obj.text
    #
    if Schedule_flag or Homework_flag or addHomework_flag == True:
        idWeekday = datetime.datetime.now().weekday()
        weekdays = ['Понедельник', 'Вторник', 'Среда',
                    'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        if Homework_flag == True:
            db.changeUserHomewFlag(event.obj.from_id, False)
            if msg == 'На сегодня':
                send_homework(event, db, weekdays[idWeekday], 1, True)
            elif msg == 'На завтра':
                if idWeekday == 6:
                    send_homework(event, db, weekdays[0], 2)
                else:
                    send_homework(event, db, weekdays[idWeekday + 1], 2)
            db.changeUserHomewFlag(event.obj.from_id, False)
        elif Schedule_flag == True:
            db.changeUserSchedFlag(event.obj.from_id, False)
            if msg == 'На сегодня':
                send_schedule(event, db, weekdays[idWeekday])
            elif msg == 'На завтра':
                if idWeekday == 6:
                    send_schedule(event, db, weekdays[0])
                else:
                    send_schedule(event, db, weekdays[idWeekday + 1])
        elif addHomework_flag == True:
            if idWeekday == 6:
                weekday = weekdays[0]
                date = get_date_by_weekday(weekday)
                db.add_HomeworkObjectToStack(
                    event.obj.from_id, date, weekday, '', '')
            else:
                weekday = weekdays[idWeekday + 1]
                date = get_date_by_weekday(weekday)
                db.add_HomeworkObjectToStack(
                    event.obj.from_id, date, weekday, '', '')
            db.changeUserStepCode(event.obj.from_id, 1)
            get_lesson(event)


def accusative_weekday(weekday) -> str:
    '''Функция перевода названия дня недели в винительный падеж, если это требуется.'''
    if weekday == 'Среда':
        return 'Среду'
    elif weekday == 'Пятница':
        return 'Пятницу'
    elif weekday == 'Суббота':
        return 'Субботу'
    else:
        return weekday


def set_weekday(user_id, db, value=None):
    '''Функция сохранения дня недели в стак в БД.'''
    if value == None:
        date = db.HomeworkStack_getDate(user_id)
        idWeekday = datetime.datetime.strptime(date, '%d.%m.%Y').weekday()
        weekdays = ['Понедельник', 'Вторник', 'Среда',
                    'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        db.HomeworkStack_setWeekday(user_id, weekdays[idWeekday])
    else:
        db.HomeworkStack_setWeekday(user_id, value)
        date = get_date_by_weekday(value)
        db.HomeworkStack_setDate(user_id, value)


def get_date_by_weekday(weekday: str) -> str:
    '''Функция получения даты по дню недели.'''
    weekdays = ['Понедельник', 'Вторник', 'Среда',
                'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    idSecondWeekday = weekdays.index(weekday)
    now = datetime.datetime.now()
    idThisWeekday = now.weekday()
    #
    if idSecondWeekday <= idThisWeekday:
        delt = (6 - idThisWeekday) + idSecondWeekday
        dur_days = datetime.timedelta(days=(delt + 1))
        result = now + dur_days
        date = result.strftime('%d.%m.%Y')
        return date
    elif idSecondWeekday > idThisWeekday:
        delt = idSecondWeekday - idThisWeekday
        dur_days = datetime.timedelta(days=delt)
        result = now + dur_days
        date = result.strftime('%d.%m.%Y')
        return date


def get_weekday_by_date(date: datetime.datetime) -> str:
    '''Функция получения дня недели по дате.'''
    idWeekday = date.weekday()
    weekdays = ['Понедельник', 'Вторник', 'Среда',
                'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    return weekdays[idWeekday]


def get_weekday_id(weekday: str) -> int:
    '''Функция получения ID дня недели.'''
    weekdays = ['Понедельник', 'Вторник', 'Среда',
                'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    return weekdays.index(weekday)


def different_operation(event, db):
    '''Функция, проводящая определенные операции, в зависимости от того что написал пользователь и при каком условии.'''
    msg = event.obj.text
    Homework_flag = db.getUserHomewFlag(event.obj.from_id)
    addHomework_flag = db.getUserAddHomewFlag(event.obj.from_id)
    delHomework_flag = db.getUserDelHomewFlag(event.obj.from_id)
    editHomework_flag = db.getUserEditHomewFlag(event.obj.from_id)
    step_code = db.getUserStepCode(event.obj.from_id)
    #
    if addHomework_flag or delHomework_flag or Homework_flag or editHomework_flag == True:
        # Date
        if step_code == 0:
            if check_date(msg) == True:
                if len(msg) == 9:
                    msg = '0' + msg
                db.add_HomeworkObjectToStack(
                    event.obj.from_id, msg, '', '', '')
                set_weekday(event.obj.from_id, db)
                if Homework_flag == True:
                    send_homework(event, db, None, 3)
                    db.changeUserHomewFlag(event.obj.from_id, False)
                elif addHomework_flag or delHomework_flag == True:
                    db.changeUserStepCode(event.obj.from_id, 1)
                    get_lesson(event)
                elif editHomework_flag == True:
                    db.changeUserStepCode(event.obj.from_id, 1)
                    send_edit_help_text(event)
            else:
                msg = 'Ошибка даты: неверный формат.'
                write_msg(event.obj.from_id, msg)
                get_date(event)
        if check_user_is_admin(event.obj.from_id) == True:
            # Lesson
            if step_code == 1:
                if editHomework_flag == True:
                    edit_homework(event, db, msg)
                elif check_lesson_text(msg) == True:
                    if addHomework_flag == True:
                        db.HomeworkStack_setLesson(event.obj.from_id, msg)
                        db.changeUserStepCode(event.obj.from_id, 2)
                        get_task(event)
                    elif delHomework_flag == True:
                        db.HomeworkStack_setLesson(event.obj.from_id, msg)
                        db.changeUserStepCode(event.obj.from_id, 0)
                        db.changeUserDelHomewFlag(event.obj.from_id, False)
                        delete_homework(event, event.obj.from_id, db)
                        db.del_HomeworkObjectFromStack(event.obj.from_id)
                else:
                    msg = 'Ошибка названия урока: длина не может превышать 16 символов.'
                    write_msg(event.obj.from_id, msg)
                    get_lesson(event)
            # Task
            elif step_code == 2:
                if check_task_text(msg) == True:
                    msg = msg.replace('''&quot;''', '''"''')
                    db.HomeworkStack_setTask(event.obj.from_id, msg)
                    db.changeUserStepCode(event.obj.from_id, 0)
                    db.changeUserAddHomewFlag(event.obj.from_id, False)
                    set_homework(event, event.obj.from_id, db)
                    db.del_HomeworkObjectFromStack(event.obj.from_id)
                else:
                    msg = 'Ошибка задач: длина не может превышать 512 символов.'
                    write_msg(event.obj.from_id, msg)
                    get_task(event)
    else:
        msg = 'Данной команды не существует.'
        write_msg(event.obj.from_id, msg)


def send_schedule(event, db, weekday):
    '''Функция отправки пользователю расписания.'''
    if weekday == 'Воскресенье':
        msg = 'Уроки в воскресенье? Всё нормально? Лучше поспи, отдохни, хорошо покушай.'
        write_msg_withKeyboard(
            event.obj.from_id, msg, get_main_menu_keyboard(event.obj.from_id))
        return
    #
    lessons = []
    weekConfig = scripts.config_pars.get_week_config(config.PATH_SETTINGS)
    if get_weekday_id(weekday) >= datetime.datetime.now().weekday():
        lessons = db.get_Lessons(weekday, weekConfig)
    else:
        if weekConfig == '1':
            lessons = db.get_Lessons(weekday, '2')
        elif weekConfig == '2':
            lessons = db.get_Lessons(weekday, '1')
    #
    listLessons = []
    for lesson in lessons:
        start_time = lesson[1]
        end_time = lesson[2]
        lesson_name = lesson[3]
        cabinet = lesson[4]
        lesson_row = f"🔹 {lesson_name} {start_time}-{end_time} | {cabinet}"
        listLessons.append(lesson_row)
    msg = '📚 Расписание уроков на {0}:'.format(accusative_weekday(weekday))
    for row in listLessons:
        msg += '\n' + row
    write_msg_withKeyboard(event.obj.from_id, msg,
                           get_main_menu_keyboard(event.obj.from_id))


def send_homework(event, db, weekday=None, mode=0, today=False):
    '''Функция отправки домашнего задания на определенный день или дату.'''
    msg = ''
    date = None
    #
    if weekday != None:
        if today == True:
            date = datetime.datetime.now().strftime('%d.%m.%Y')
        else:
            date = get_date_by_weekday(weekday)
    else:
        date = db.HomeworkStack_getDate(event.obj.from_id)
        weekday = db.HomeworkStack_getWeekday(event.obj.from_id)
    #
    date_type = datetime.datetime.strptime(date, '%d.%m.%Y')
    #
    now = datetime.datetime.now().replace(
        hour=0, second=0, microsecond=0, minute=0)
    delt = 7 + datetime.datetime.now().weekday()
    dur_days = datetime.timedelta(days=(delt))
    dStartLastWeek = now - dur_days
    if dStartLastWeek > date_type:
        msg = 'Вы пытаетесь посмотреть домашнее задание на давний срок. В главной базе данных хранятся все домашние \
               задания начиная с прошлой недели. Чтобы всё-таки узнать нужное вам домашнее задание, можете обратиться к \
               администратору - @3x0d2s(Максим Жданов).'
        db.del_HomeworkObjectFromStack(event.obj.from_id)
        write_msg_withKeyboard(
            event.obj.from_id, msg, get_main_menu_keyboard(event.obj.from_id))
        return
    #
    if weekday != 'Воскресенье':
        homework_tasks = db.get_Homework(date)
        rowcount = len(homework_tasks)
        if rowcount > 0:
            listHomework = []
            for row in range(rowcount):
                lesson_name = homework_tasks[row][0]
                task = homework_tasks[row][1]
                if check_new_line_in_task_text(task) == True:
                    msg = str('🔺 {0}:\n{1}'.format(lesson_name, task))
                else:
                    msg = str('🔺 {0}: {1}'.format(lesson_name, task))
                listHomework.append(msg)
            msg = '📝 Домашнее задание на {0} ({1}):'.format(
                accusative_weekday(weekday), date)
            for rows in listHomework:
                msg += '\n' + rows
        else:
            if mode == 0:
                if weekday == 'Понедельник' or weekday == 'Вторник' or weekday == 'Четверг':
                    msg = 'На ближайший {0} нет домашнего задания.'.format(
                        weekday.lower())
                else:
                    msg = 'На ближайшую {0} нет домашнего задания.'.format(
                        accusative_weekday(weekday).lower())
            elif mode == 1:
                msg = 'На сегодня нет домашнего задания.'
            elif mode == 2:
                msg = 'На завтра нет домашнего задания.'
            elif mode == 3:
                if weekday == 'Понедельник' or weekday == 'Вторник' or weekday == 'Четверг':
                    msg = 'На {0} {1} нет домашнего задания.'.format(
                        weekday.lower(), date)
                else:
                    msg = 'На {0} {1} нет домашнего задания.'.format(
                        accusative_weekday(weekday).lower(), date)
    elif weekday == 'Воскресенье':
        msg = 'Домашнее задание на воскресенье? Совсем переучились?'
    db.del_HomeworkObjectFromStack(event.obj.from_id)
    #
    if event.obj.from_id != None:
        write_msg_withKeyboard(event.obj.from_id, msg,
                               get_main_menu_keyboard(event.obj.from_id))
    else:
        vk.messages.edit(
            peer_id=event.obj.peer_id,
            message=msg,
            conversation_message_id=event.obj.conversation_message_id,
            keyboard=get_main_menu_keyboard(event.obj.user_id).get_keyboard(),
        )
    #
    if mode == 2 and weekday != 'Воскресенье':
        db.add_user_in_homework_f(event.obj.from_id)


def set_homework(event, user_id, db):
    '''Функция добавления домашнего задания в БД.'''
    date = db.HomeworkStack_getDate(user_id)
    weekDay = db.HomeworkStack_getWeekday(user_id)
    lesson = db.HomeworkStack_getLesson(user_id)
    task = db.HomeworkStack_getTask(user_id)
    #
    if weekDay == 'Воскресенье':
        msg = 'Домашнее задание на воскресенье? Может не надо?'
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Добавить домашнее задание',
                            color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
        write_msg_withKeyboard(event.obj.from_id, msg, keyboard)
        return
    #
    if db.check_Homework(date, lesson) == False:
        db.add_Homework(date, weekDay, lesson, task)
        if db.check_Homework(date, lesson) == True:
            msg = 'Домашнее задание добавлено!'
            write_msg_withKeyboard(
                event.obj.from_id, msg, get_main_menu_keyboard(event.obj.from_id))
            #
            today = datetime.datetime.now()
            tomorrow = today + datetime.timedelta(days=1)
            strftomorrow = tomorrow.strftime('%d.%m.%Y')
            if date == strftomorrow:
                mailing_notifications_about_new_homework(db, user_id)
        else:
            msg = 'Домашнее задание не было добавлено.'
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button('Добавить домашнее задание',
                                color=VkKeyboardColor.SECONDARY)
            keyboard.add_line()
            keyboard.add_button(
                'В главное меню', color=VkKeyboardColor.POSITIVE)
            write_msg_withKeyboard(event.obj.from_id, msg, keyboard)
    else:
        msg = 'Домашнее задание по этому предмету уже записано на указанный день.'
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Добавить домашнее задание',
                            color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
        write_msg_withKeyboard(event.obj.from_id, msg, keyboard)


def mailing_notifications_about_new_homework(db, user_id):
    '''Функция рассылки оповещения о новом домашнем задании на завтра людям, предварительно сегодня посмотревших ДЗ на завтрашний день.'''
    users = db.get_users_in_homework_f()
    #
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_callback_button(
        label="Посмотреть",
        color=VkKeyboardColor.POSITIVE,
        payload={"type": "show_homework_tomorrow"},
    )
    #
    msg = 'Внимание, на завтра было добавлено новое домашнее задание.'
    #
    for user in users:
        if user_id != user[0]:  # если пользователь не тот, кто добавил домашнее задание
            write_msg_withKeyboard(user[0], msg, keyboard)


def delete_homework(event, user_id, db):
    '''Функция удаления домашнего задания из БД.'''
    date = db.HomeworkStack_getDate(user_id)
    lesson = db.HomeworkStack_getLesson(user_id)
    #
    if db.check_Homework(date, lesson) == True:
        db.del_Homework(date, lesson)
        msg = 'Домашнее задание удалено!'
        write_msg_withKeyboard(
            event.obj.from_id, msg, get_main_menu_keyboard(event.obj.from_id))
    else:
        msg = 'Такого домашнего задания не существует.'
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Удаление домашнего задания',
                            color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
        write_msg_withKeyboard(event.obj.from_id, msg, keyboard)


def edit_homework(event, db, msg):
    '''Функция редактирования ДЗ.'''
    result_text = ''
    error = True
    pattern_1 = re.compile('::')  # For change task
    pattern_2 = re.compile('@@')  # For change date
    if pattern_1.findall(msg):
        сommand_parts = msg.split('::', maxsplit=1)
        lesson_h = сommand_parts[0]
        task_h = сommand_parts[1]
        if len(task_h) != 0 and task_h[0] == '\n':
            task_h = task_h.replace('\n', '', 1)
        task_h = task_h.replace('''&quot;''', '''"''')
        #
        if len(lesson_h) == 0:
            result_text += 'Ошибка: вы не указали название урока.\n'
        if len(task_h) == 0:
            result_text += 'Ошибка: вы не указали измененное задание.\n'
        if check_lesson_text(lesson_h) == False:
            result_text += 'Ошибка названия урока: длина не может превышать 32 символа.\n'
        if check_task_text(task_h) == False:
            result_text += 'Ошибка текста задания: длина не может превышать 512 символов.\n'
        if result_text == '':
            error = False
            date_h = db.HomeworkStack_getDate(
                event.obj.from_id)
            if db.check_Homework(date_h, lesson_h) == True:
                db.editTaskForHomework(date_h, lesson_h, task_h)
                result_text = 'Домашнее задание было отредактировано.'
            else:
                result_text = 'Указанное домашнее задание не существует.'
    elif pattern_2.findall(msg):
        сommand_parts = msg.split('@@', maxsplit=1)
        lesson_h = сommand_parts[0]
        date_h_new = сommand_parts[1]
        date_h_new = date_h_new.replace(' ', '')
        if len(date_h_new) == 9:
            date_h_new = '0' + date_h_new
        #
        if datetime.datetime.strptime(date_h_new, '%d.%m.%Y').weekday() == 6:
            result_text += 'Ошибка: вы пытаетесь добавить домашнее задание на воскресенье.'
        if len(lesson_h) == 0:
            result_text += 'Ошибка: вы не указали название урока.\n'
        if len(date_h_new) == 0:
            result_text += 'Ошибка: вы не указали новую дату.\n'
        if check_lesson_text(lesson_h) == False:
            result_text += 'Ошибка названия урока: длина не может превышать 32 символа.\n'
        if check_date(date_h_new) == False:
            result_text += 'Ошибка даты: неверный формат.\n'
        if result_text == '':
            error = False
            date_h_old = db.HomeworkStack_getDate(event.obj.from_id)
            if db.check_Homework(date_h_old, lesson_h) == True:
                db.editDateForHomework(date_h_old, lesson_h, date_h_new)
                result_text = 'Домашнее задание было отредактировано.'
            else:
                result_text = 'Указанное домашнее задание не существует.'
    else:
        result_text = 'Ошибка формата команды.'
    #
    if error == True:
        write_msg(event.obj.from_id, result_text)
        send_edit_help_text(event)
    else:
        db.del_HomeworkObjectFromStack(event.obj.from_id)
        db.changeUserStepCode(event.obj.from_id, 0)
        db.changeUserEditHomewFlag(event.obj.from_id, False)
        write_msg_withKeyboard(event.obj.from_id, result_text,
                               get_main_menu_keyboard(event.obj.from_id))


def send_homework_on_week(event, db, mode):
    ''' Функция отправки всего домашнего задания на определенную неделю.

        mode:
        0 - this week
        1 - next week'''
    allHomework = db.get_allHomework()
    #
    if len(allHomework) == 0:
        if mode == 0:
            output = 'Домашнее задание на эту неделю не было найдено.'
            write_msg_withKeyboard(event.obj.from_id, output,
                                   get_main_menu_keyboard(event.obj.from_id))
        elif mode == 1:
            output = 'Домашнее задание на следующую неделю не было найдено.'
            write_msg_withKeyboard(event.obj.from_id, output,
                                   get_main_menu_keyboard(event.obj.from_id))
        return
    #
    if mode == 0:
        output = '📝 Всё домашнее задание до конца этой недели:\n'
        list_h = []
        now = datetime.datetime.now()
        weekday = now.weekday()
        #
        delt = (7 - weekday)
        dur_days = datetime.timedelta(days=(delt))
        result = now + dur_days
        dateStartNextWeek = result.strftime('%d.%m.%Y')
        dateStartNextWeek = datetime.datetime.strptime(
            dateStartNextWeek, '%d.%m.%Y')
        #
        for row in allHomework:
            date = datetime.datetime.strptime(row[0], '%d.%m.%Y')
            if date > now and date < dateStartNextWeek:
                weekday_h = get_weekday_by_date(date)
                lesson_name = row[1]
                task = row[2]
                list_h.append([date, lesson_name, weekday_h, task])
        if len(list_h) == 0:
            output = 'Домашнее задание на эту неделю не было найдено.'
        else:
            weekdays = ['Понедельник', 'Вторник', 'Среда',
                        'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
            homew_goto = []
            for i in range(7):
                for homew in list_h:
                    if homew[2] == weekdays[i] and homew not in homew_goto:
                        if check_new_line_in_task_text(task) == True:
                            output += str('🔺 {0} на {1}:\n{2}\n'.format(
                                homew[1], accusative_weekday(homew[2]).lower(), homew[3]))
                        else:
                            output += str('🔺 {0} на {1}: {2}\n'.format(
                                homew[1], accusative_weekday(homew[2]).lower(), homew[3]))
                        homew_goto.append(homew)
    elif mode == 1:
        output = '📝 Всё домашнее задание на следующую неделю:\n'
        list_h = []
        now = datetime.datetime.now()
        weekday = now.weekday()
        #
        delt = (7 - weekday)
        dur_days = datetime.timedelta(days=(delt))
        result = now + dur_days
        dateStartNextWeek = result.strftime('%d.%m.%Y')
        dateStartNextWeek = datetime.datetime.strptime(
            dateStartNextWeek, '%d.%m.%Y')
        #
        dur_days = datetime.timedelta(days=(7))
        result += dur_days
        dateStartNextNextWeek = result.strftime('%d.%m.%Y')
        dateStartNextNextWeek = datetime.datetime.strptime(
            dateStartNextNextWeek, '%d.%m.%Y')
        #
        for row in allHomework:
            date = datetime.datetime.strptime(row[0], '%d.%m.%Y')
            if date >= dateStartNextWeek and date < dateStartNextNextWeek:
                weekday_h = get_weekday_by_date(date)
                lesson_name = row[1]
                task = row[2]
                list_h.append([date, lesson_name, weekday_h, task])
        #
        if len(list_h) == 0:
            output = 'Домашнее задание на следующую неделю не было найдено.'
        else:
            weekdays = ['Понедельник', 'Вторник', 'Среда',
                        'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
            homew_goto = []
            for i in range(7):
                for homew in list_h:
                    if homew[2] == weekdays[i] and homew not in homew_goto:
                        if check_new_line_in_task_text(task) == True:
                            output += str('🔺 {0} на {1}:\n{2}\n'.format(
                                homew[1], accusative_weekday(homew[2]).lower(), homew[3]))
                        else:
                            output += str('🔺 {0} на {1}: {2}\n'.format(
                                homew[1], accusative_weekday(homew[2]).lower(), homew[3]))
                        homew_goto.append(homew)
    #
    write_msg_withKeyboard(event.obj.from_id, output,
                           get_main_menu_keyboard(event.obj.from_id))


def check_new_line_in_task_text(task) -> bool:
    '''Проверка новой строки в тексте задания.'''
    pattern = re.compile(r'\n')
    if pattern.findall(task):
        return True
    return False


def write_msg(user_id, message):
    '''Функция отправки сообщения без клавиатуры.'''
    vk_session.method('messages.send', {
                      'user_id': user_id, 'message': str(message), 'random_id': 0})


def write_msg_withKeyboard(user_id, message, keyboard):
    '''Функция отправки сообщения с клавиатурой.'''
    vk_session.method('messages.send', {'user_id': user_id, 'message': str(message),
                                        'random_id': 0, 'keyboard': keyboard.get_keyboard()})


def get_main_menu_keyboard(user_id) -> VkKeyboard:
    '''Функция генерации главной клавиатуры.'''
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Расписание', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Домашнее задание', color=VkKeyboardColor.POSITIVE)
    if check_user_is_admin(user_id) == True:
        keyboard.add_line()
        keyboard.add_button(
            'Редактирование', color=VkKeyboardColor.SECONDARY)
    return keyboard


def get_editing_keyboard() -> VkKeyboard:
    '''Функция генерации клавиатуры редактирования. Только для администраторов.'''
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Добавить домашнее задание',
                        color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Редактировать домашнее задание',
                        color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Удаление домашнего задания',
                        color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
    return keyboard


def send_homework_on_week_text_and_keyboard(event):
    '''Генерирует клавиатуру для выбора недели, на которую нужно прислать ДЗ, и отсылает её.'''
    date_now = datetime.datetime.now()
    weekday_now = get_weekday_by_date(date_now)
    if weekday_now not in ('Суббота', 'Воскресенье'):
        msg = 'Выберите...'
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('На эту', color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('На следующую', color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
        write_msg_withKeyboard(event.obj.from_id, msg, keyboard)
    else:
        db = requestDB(config.PATH_DB)
        send_homework_on_week(event, db, 1)
        db.changeUserHomewFlag(event.obj.from_id, False)
        db.close()


def get_users(db):
    '''Функция получения всех пользователей из БД.'''
    global users
    users = db.get_users()


def check_is_new_user(user_id: int) -> bool:
    "Проверяет нет ли пользователя в БД."
    global users
    if len(users) != 0:
        isNewUser = True
        for user in users:
            if user_id == user[0]:
                isNewUser = False
                break
        return isNewUser
    else:  # Если пользователь - первый, кто написал боту
        return True


def user_processing(user_id: int):
    "Обработка пользователя, написавшего боту."
    if check_is_new_user(user_id) == True:
        db = requestDB(config.PATH_DB)
        db.add_user(user_id)
        get_users(db)
        db.close()


def check_user_is_admin(user_id) -> bool:
    '''Проверяет администратор ли пользователь.'''
    for user in range(len(users)):
        if user_id == users[user][0]:
            return users[user][1]  # True or False


def send_edit_help_text(event):
    '''Отправляет текстовое сообщения с инструкцией для редактирования ДЗ.'''
    msg = 'Введите команду в формате:\n🔺 Для изменения задания:\n(Название урока)::(Новое задание)\n🔺 Для изменения даты:\n(Название урока)@@(Новая дата)'
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    write_msg_withKeyboard(event.obj.from_id, msg, keyboard)


def send_editing_text_and_keyboard(event):
    '''Отправляет сообщения с клавиатурой редактирования.'''
    msg = 'Выберите действие...'
    write_msg_withKeyboard(event.obj.from_id, msg, get_editing_keyboard())


def get_date(event):
    '''Функция, которая предлагает пользователю ввести дату.'''
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    msg = 'Введите число в формате (День).(Месяц).(Год). Например 03.11.2018'
    write_msg_withKeyboard(event.obj.from_id, msg, keyboard)


def get_lesson(event):
    '''Функция, которая предлагает пользователю ввести название урока.'''
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    msg = 'Введите название урока...'
    write_msg_withKeyboard(event.obj.from_id, msg, keyboard)


def get_task(event):
    '''Функция, которая предлагает пользователю ввести задачу.'''
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    msg = 'Введите все задачи...'
    write_msg_withKeyboard(event.obj.from_id, msg, keyboard)


# @logger.catch
def check_command(event):
    '''Функция, проверяющая команду от пользователя и запускающая определенный сценарий.'''
    msg = event.obj.text
    db = requestDB(config.PATH_DB)
    Homework_flag = db.getUserHomewFlag(event.obj.from_id)
    Schedule_flag = db.getUserSchedFlag(event.obj.from_id)
    addHomework_flag = db.getUserAddHomewFlag(event.obj.from_id)
    delHomework_flag = db.getUserDelHomewFlag(event.obj.from_id)
    editHomework_flag = db.getUserEditHomewFlag(event.obj.from_id)
    #
    if msg == 'Домашнее задание':
        db.changeUserHomewFlag(event.obj.from_id, True)
        show_weekdays(event.obj.from_id, db)
    elif msg == 'Расписание':
        db.changeUserSchedFlag(event.obj.from_id, True)
        show_weekdays(event.obj.from_id, db)
    elif msg == 'На сегодня' or msg == 'На завтра':
        operation_today_or_tomorrow(event, db)
    elif msg in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']:
        operations_with_weekdays(event, db)
    elif msg == 'В главное меню':
        if Schedule_flag == True:
            db.changeUserSchedFlag(event.obj.from_id, False)
        elif Homework_flag == True:
            db.changeUserHomewFlag(event.obj.from_id, False)
        elif addHomework_flag == True:
            db.del_HomeworkObjectFromStack(event.obj.from_id)
            db.changeUserAddHomewFlag(event.obj.from_id, False)
        elif delHomework_flag == True:
            db.del_HomeworkObjectFromStack(event.obj.from_id)
            db.changeUserDelHomewFlag(event.obj.from_id, False)
        write_msg_withKeyboard(
            event.obj.from_id, 'Главное меню', get_main_menu_keyboard(event.obj.from_id))
    elif msg == 'На неделю':
        if Homework_flag == True:
            send_homework_on_week_text_and_keyboard(event)
    elif msg == 'На эту':
        send_homework_on_week(event, db, 0)
        db.changeUserHomewFlag(event.obj.from_id, False)
    elif msg == 'На следующую':
        send_homework_on_week(event, db, 1)
        db.changeUserHomewFlag(event.obj.from_id, False)
    elif msg == 'Указать число':
        if Homework_flag or addHomework_flag == True:
            get_date(event)
    elif msg == 'Редактирование':
        if check_user_is_admin(event.obj.from_id) == True:
            send_editing_text_and_keyboard(event)
    elif msg == 'Добавить домашнее задание':
        if check_user_is_admin(event.obj.from_id) == True:
            db.changeUserAddHomewFlag(event.obj.from_id, True)
            show_weekdays(event.obj.from_id, db)
    elif msg == 'Редактировать домашнее задание':
        if check_user_is_admin(event.obj.from_id) == True:
            db.changeUserEditHomewFlag(event.obj.from_id, True)
            get_date(event)
    elif msg == 'Удаление домашнего задания':
        if check_user_is_admin(event.obj.from_id) == True:
            db.changeUserDelHomewFlag(event.obj.from_id, True)
            get_date(event)
    elif msg == 'Отмена':
        if addHomework_flag == True:
            db.del_HomeworkObjectFromStack(event.obj.from_id)
            db.changeUserAddHomewFlag(event.obj.from_id, False)
            db.changeUserStepCode(event.obj.from_id, 0)
        elif delHomework_flag == True:
            db.del_HomeworkObjectFromStack(event.obj.from_id)
            db.changeUserDelHomewFlag(event.obj.from_id, False)
            db.changeUserStepCode(event.obj.from_id, 0)
        elif Homework_flag == True:
            db.del_HomeworkObjectFromStack(event.obj.from_id)
            db.changeUserHomewFlag(event.obj.from_id, False)
            db.changeUserStepCode(event.obj.from_id, 0)
        elif editHomework_flag == True:
            db.del_HomeworkObjectFromStack(event.obj.from_id)
            db.changeUserStepCode(event.obj.from_id, 0)
            db.changeUserEditHomewFlag(event.obj.from_id, False)
        write_msg_withKeyboard(
            event.obj.from_id, 'Главное меню', get_main_menu_keyboard(event.obj.from_id))
    elif msg == 'Начать':
        write_msg_withKeyboard(
            event.obj.from_id, 'Главное меню', get_main_menu_keyboard(event.obj.from_id))
    else:
        different_operation(event, db)
    db.close()


def main():
    '''Главная функция инициализации и запуска бота.'''
    global vk_session, session_api, longpoll, users, vk
    #
    vk_session = VkApi(token=config.TOKEN)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=config.GROUP_ID)
    #
    users = None
    #
    logger.add('Debug.log', format="{time} {level} {message}",
               level="DEBUG", rotation="1 week", compression="zip")
    #
    # Create a Data Base from a dump file if db.db isn't exists
    if not os.path.isfile(config.PATH_DB):
        from scripts.request_db import createBD_FromDump
        createBD_FromDump(config.PATH_DB, config.PATH_DUMP)
    #
    db = requestDB(config.PATH_DB)
    get_users(db)
    db.close()
    #
    for event in longpoll.listen():
        #
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.from_user:
                user_processing(event.obj.from_id)
                check_command(event)
        #
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            #
            if event.object.payload.get("type") == "show_homework_tomorrow":
                db = requestDB(config.PATH_DB)
                idWeekday = datetime.datetime.now().weekday()
                weekdays = ['Понедельник', 'Вторник', 'Среда',
                            'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
                #
                if idWeekday == 6:
                    send_homework(event, db, weekdays[0], 2)
                else:
                    send_homework(event, db, weekdays[idWeekday + 1], 2)
                #
                db.close()


if __name__ == '__main__':
    main()
