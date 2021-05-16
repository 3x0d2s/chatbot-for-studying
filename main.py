#
import re
import os
import datetime
#
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from loguru import logger
#
import config.config as config
from scripts.request_db import requestDB
from scripts.check_InputData import *
import scripts.config_pars
#
vk_session = vk_api.VkApi(token=config.token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
users = None
#
logger.add('Debug.log', format="{time} {level} {message}",
           level="DEBUG", rotation="1 week", compression="zip")
#


def show_weekdays(event, db):
    Homework_flag = db.getUserHomewFlag(event.user_id)
    Schedule_flag = db.getUserSchedFlag(event.user_id)
    addHomework_flag = db.getUserAddHomewFlag(event.user_id)
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
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def operations_with_weekdays(event, db, msg):
    addHomework_flag = db.getUserAddHomewFlag(event.user_id)
    Homework_flag = db.getUserHomewFlag(event.user_id)
    Schedule_flag = db.getUserSchedFlag(event.user_id)
    delHomework_flag = db.getUserDelHomewFlag(event.user_id)
    step_code = db.getUserStepCode(event.user_id)
    #
    if Homework_flag == True:
        send_homework(event, db, msg)
        db.changeUserHomewFlag(event.user_id, False)
    elif Schedule_flag == True:
        send_schedule(db, msg)
        db.changeUserSchedFlag(event.user_id, False)
    elif addHomework_flag == True or delHomework_flag == True:
        weekday = msg
        date = get_date_by_weekday(weekday)
        db.add_HomeworkObjectToStack(event.user_id, date, weekday, '', '')
        db.changeUserStepCode(event.user_id, (step_code + 1))
        set_lesson()


def operation_today_or_tomorrow(event, db):
    Schedule_flag = db.getUserSchedFlag(event.user_id)
    Homework_flag = db.getUserHomewFlag(event.user_id)
    addHomework_flag = db.getUserAddHomewFlag(event.user_id)
    #
    if Schedule_flag == True or Homework_flag == True or addHomework_flag == True:
        idWeekday = datetime.datetime.now().weekday()
        weekdays = ['Понедельник', 'Вторник', 'Среда',
                    'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        if Homework_flag == True:
            db.changeUserHomewFlag(event.user_id, False)
            if msg == 'На сегодня':
                send_homework(event, db, weekdays[idWeekday], 1, True)
            elif msg == 'На завтра':
                if idWeekday == 6:
                    send_homework(event, db, weekdays[0], 2)
                else:
                    send_homework(event, db, weekdays[idWeekday + 1], 2)
            db.changeUserHomewFlag(event.user_id, False)
        elif Schedule_flag == True:
            db.changeUserSchedFlag(event.user_id, False)
            if msg == 'На сегодня':
                send_schedule(db, weekdays[idWeekday])
            elif msg == 'На завтра':
                if idWeekday == 6:
                    send_schedule(db, weekdays[0])
                else:
                    send_schedule(db, weekdays[idWeekday + 1])
        elif addHomework_flag == True:
            if idWeekday == 6:
                weekday = weekdays[0]
                date = get_date_by_weekday(weekday)
                db.add_HomeworkObjectToStack(
                    event.user_id, date, weekday, '', '')
            else:
                weekday = weekdays[idWeekday + 1]
                date = get_date_by_weekday(weekday)
                db.add_HomeworkObjectToStack(
                    event.user_id, date, weekday, '', '')
            db.changeUserStepCode(event.user_id, 1)
            set_lesson()


def accusative_weekday(weekday) -> str:
    if weekday == 'Среда':
        return 'Среду'
    elif weekday == 'Пятница':
        return 'Пятницу'
    elif weekday == 'Суббота':
        return 'Субботу'
    else:
        return weekday


def set_weekday(user_id, db, value=None):
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
        return date
    elif idSecondWeekday > idThisWeekday:
        delt = idSecondWeekday - idThisWeekday
        dur_days = datetime.timedelta(days=delt)
        result = now + dur_days
        date = result.strftime('%d.%m.%Y')
        return date


def get_weekday_by_date(date: datetime.datetime) -> str:
    idWeekday = date.weekday()
    weekdays = ['Понедельник', 'Вторник', 'Среда',
                'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    return weekdays[idWeekday]


def different_operation(event, db, msg):
    Homework_flag = db.getUserHomewFlag(event.user_id)
    addHomework_flag = db.getUserAddHomewFlag(event.user_id)
    delHomework_flag = db.getUserDelHomewFlag(event.user_id)
    editHomework_flag = db.getUserEditHomewFlag(event.user_id)
    step_code = db.getUserStepCode(event.user_id)
    #
    if addHomework_flag or delHomework_flag or Homework_flag or editHomework_flag == True:
        # Date
        if step_code == 0:
            if Check_Date(msg) == True:
                if len(msg) == 9:
                    msg = '0' + msg
                db.add_HomeworkObjectToStack(event.user_id, msg, '', '', '')
                set_weekday(event.user_id, db)
                if Homework_flag == True:
                    send_homework(event, db, None, 3)
                    db.changeUserHomewFlag(event.user_id, False)
                elif addHomework_flag or delHomework_flag == True:
                    db.changeUserStepCode(event.user_id, 1)
                    set_lesson()
                elif editHomework_flag == True:
                    db.changeUserStepCode(event.user_id, 1)
                    get_edit_command(event)
            else:
                msg = 'Ошибка даты: неверный формат.'
                write_msg(event.user_id, msg)
                set_date()
        if user_is_admin_check(event) == True:
            # Lesson
            if step_code == 1:
                if editHomework_flag == True:
                    edit_homework(event, db, msg)
                elif Check_Lesson(msg) == True:
                    if addHomework_flag == True:
                        db.HomeworkStack_setLesson(event.user_id, msg)
                        db.changeUserStepCode(event.user_id, 2)
                        set_task()
                    elif delHomework_flag == True:
                        db.HomeworkStack_setLesson(event.user_id, msg)
                        db.changeUserStepCode(event.user_id, 0)
                        db.changeUserDelHomewFlag(event.user_id, False)
                        delete_homework(event.user_id, db)
                        db.del_HomeworkObjectFromStack(event.user_id)
                else:
                    msg = 'Ошибка названия урока: длина не может превышать 16 символов.'
                    write_msg(event.user_id, msg)
                    set_lesson()
            # Task
            elif step_code == 2:
                if Check_Tasks(msg) == True:
                    msg = msg.replace('''&quot;''', '''"''')
                    db.HomeworkStack_setTask(event.user_id, msg)
                    db.changeUserStepCode(event.user_id, 0)
                    db.changeUserAddHomewFlag(event.user_id, False)
                    set_homework(event.user_id, db)
                    db.del_HomeworkObjectFromStack(event.user_id)
                else:
                    msg = 'Ошибка задач: длина не может превышать 512 символов.'
                    write_msg(event.user_id, msg)
                    set_task()
    else:
        msg = 'Данной команды не существует.'
        write_msg(event.user_id, msg)


def send_schedule(db, weekday):
    if weekday == 'Воскресенье':
        msg = 'Уроки в воскресенье? Всё нормально? Лучше поспи, отдохни, хорошо покушай.'
        write_msg_withKeyboard(
            event.user_id, msg, get_main_menu_keyboard(event))
        return
    #
    weekConfig = scripts.config_pars.getWeekConfig(config.PATH_SETTINGS)
    if get_weekday_id(weekday) >= datetime.datetime.now().weekday():
        lesson = db.get_Lesson(weekday, weekConfig)
    else:
        if weekConfig == str(1):
            lesson = db.get_Lesson(weekday, str(2))
        elif weekConfig == str(2):
            lesson = db.get_Lesson(weekday, str(1))
    #
    listLessons = []
    rowcount = len(lesson)
    for row in range(rowcount):
        start_time = lesson[row][1]
        end_time = lesson[row][2]
        lesson_name = lesson[row][3]
        cabinet = lesson[row][4]
        msg = str('🔹 ' + lesson_name + ' ' + start_time +
                  '-' + end_time + ' | ' + str(cabinet))
        listLessons.append(msg)
    msg = '📚 Расписание уроков на {0}:'.format(accusative_weekday(weekday))
    for row in listLessons:
        msg += '\n' + row
    write_msg_withKeyboard(event.user_id, msg, get_main_menu_keyboard(event))


def get_weekday_id(weekday) -> int:
    weekdays = ['Понедельник', 'Вторник', 'Среда',
                'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    idWeekday = 0
    for w in weekdays:
        if w == weekday:
            return idWeekday
        else:
            idWeekday += 1


def send_homework(event, db, weekday=None, mode=0, today=False):
    msg = ''
    date = None
    #
    if weekday != None:
        if today == True:
            date = datetime.datetime.now().strftime('%d.%m.%Y')
        else:
            date = get_date_by_weekday(weekday)
    else:
        date = db.HomeworkStack_getDate(event.user_id)
        weekday = db.HomeworkStack_getWeekday(event.user_id)
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
        db.del_HomeworkObjectFromStack(event.user_id)
        write_msg_withKeyboard(
            event.user_id, msg, get_main_menu_keyboard(event))
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
    db.del_HomeworkObjectFromStack(event.user_id)
    write_msg_withKeyboard(event.user_id, msg, get_main_menu_keyboard(event))


def set_homework(user_id, db):
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
        write_msg_withKeyboard(event.user_id, msg, keyboard)
        return
    #
    if db.check_Homework(date, lesson) == False:
        db.add_Homework(date, weekDay, lesson, task)
        if db.check_Homework(date, lesson) == True:
            msg = 'Домашнее задание добавлено!'
            write_msg_withKeyboard(
                event.user_id, msg, get_main_menu_keyboard(event))
        else:
            msg = 'Домашнее задание не было добавлено.'
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button('Добавить домашнее задание',
                                color=VkKeyboardColor.SECONDARY)
            keyboard.add_line()
            keyboard.add_button(
                'В главное меню', color=VkKeyboardColor.POSITIVE)
            write_msg_withKeyboard(event.user_id, msg, keyboard)
    else:
        msg = 'Домашнее задание по этому предмету уже записано на указанный день.'
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Добавить домашнее задание',
                            color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
        write_msg_withKeyboard(event.user_id, msg, keyboard)


def delete_homework(user_id, db):
    date = db.HomeworkStack_getDate(user_id)
    lesson = db.HomeworkStack_getLesson(user_id)
    #
    if db.check_Homework(date, lesson) == True:
        db.del_Homework(date, lesson)
        msg = 'Домашнее задание удалено!'
        write_msg_withKeyboard(
            event.user_id, msg, get_main_menu_keyboard(event))
    else:
        msg = 'Такого домашнего задания не существует.'
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Удаление домашнего задания',
                            color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
        write_msg_withKeyboard(event.user_id, msg, keyboard)


def edit_homework(event, db, msg):
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
        if Check_Lesson(lesson_h) == False:
            result_text += 'Ошибка названия урока: длина не может превышать 32 символа.\n'
        if Check_Tasks(task_h) == False:
            result_text += 'Ошибка текста задания: длина не может превышать 512 символов.\n'
        if result_text == '':
            error = False
            date_h = db.HomeworkStack_getDate(
                event.user_id)
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
        if len(lesson_h) == 0:
            result_text += 'Ошибка: вы не указали название урока.\n'
        if len(date_h_new) == 0:
            result_text += 'Ошибка: вы не указали новую дату.\n'
        if Check_Lesson(lesson_h) == False:
            result_text += 'Ошибка названия урока: длина не может превышать 32 символа.\n'
        if Check_Date(date_h_new) == False:
            result_text += 'Ошибка даты: неверный формат.\n'
        if result_text == '':
            error = False
            date_h_old = db.HomeworkStack_getDate(
                event.user_id)
            if db.check_Homework(date_h_old, lesson_h) == True:
                db.editDateForHomework(date_h_old, lesson_h, date_h_new)
                result_text = 'Домашнее задание было отредактировано.'
            else:
                result_text = 'Указанное домашнее задание не существует.'
    else:
        result_text = 'Ошибка формата команды.'
    #
    if error == True:
        write_msg(event.user_id, result_text)
        get_edit_command(event)
    else:
        db.del_HomeworkObjectFromStack(event.user_id)
        db.changeUserStepCode(event.user_id, 0)
        db.changeUserEditHomewFlag(event.user_id, False)
        write_msg_withKeyboard(event.user_id, result_text,
                               get_main_menu_keyboard(event))


def get_homework_on_week(db, mode):
    ''' mode:
        0 - this week
        1 - next week'''
    allHomework = db.get_allHomework()
    #
    if len(allHomework) == 0:
        if mode == 0:
            output = 'Домашнее задание на эту неделю не было найдено.'
            write_msg_withKeyboard(event.user_id, output,
                                   get_main_menu_keyboard(event))
        elif mode == 1:
            output = 'Домашнее задание на следующую неделю не было найдено.'
            write_msg_withKeyboard(event.user_id, output,
                                   get_main_menu_keyboard(event))
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
    write_msg_withKeyboard(event.user_id, output,
                           get_main_menu_keyboard(event))


def check_new_line_in_task_text(task) -> bool:
    pattern = re.compile(r'\n')
    if pattern.findall(task):
        return True
    return False


def write_msg(user_id, message):
    vk_session.method('messages.send', {
                      'user_id': user_id, 'message': str(message), 'random_id': 0})


def write_msg_withKeyboard(user_id, message, keyboard):
    vk_session.method('messages.send', {'user_id': user_id, 'message': str(message),
                                        'random_id': 0, 'keyboard': keyboard.get_keyboard()})


def get_main_menu_keyboard(event) -> VkKeyboard:
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Расписание', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Домашнее задание', color=VkKeyboardColor.POSITIVE)
    if user_is_admin_check(event) == True:
        keyboard.add_line()
        keyboard.add_button(
            'Редактирование', color=VkKeyboardColor.SECONDARY)
    return keyboard


def get_editing_keyboard() -> VkKeyboard:
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


def get_users(db):
    global users
    users = db.get_users()


def check_is_new_user(user_id: int) -> bool:
    "Проверяет нет ли пользователя в БД."
    if len(users) != 0:
        isNewUser = True
        for user in users:
            if user_id == user[0]:
                isNewUser = False
                break
        return isNewUser
    else:  # Если пользователь - первый, кто написал боту
        return True


async def user_processing(user_id: int):
    "Обработка пользователя, запустившего бота."
    if check_is_new_user(user_id) == True:
        db = requestDB(config.PATH_DB)
        db.add_user(user_id)
        db.close()
        get_users()


def user_is_admin_check(event) -> bool:
    user_id = event.user_id
    for user in range(len(users)):
        if user_id == users[user][0]:
            return users[user][1]  # True or False


def homework_on_week_menu():
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
        write_msg_withKeyboard(event.user_id, msg, keyboard)
    else:
        db = requestDB(config.PATH_DB)
        get_homework_on_week(db, 1)
        db.changeUserHomewFlag(event.user_id, False)
        db.close()


def get_edit_command(event):
    msg = 'Введите команду в формате:\n🔺 Для изменения задания:\n(Название урока)::(Новое задание)\n🔺 Для изменения даты:\n(Название урока)@@(Новая дата)'
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def editing():
    msg = 'Выберите действие...'
    write_msg_withKeyboard(event.user_id, msg, get_editing_keyboard())


def set_date():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    msg = 'Введите число в формате (День).(Месяц).(Год). Например 03.11.2018'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def set_lesson():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    msg = 'Введите название урока...'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def set_task():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    msg = 'Введите все задачи...'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


@logger.catch
def check_command(event, msg):
    db = requestDB(config.PATH_DB)
    Homework_flag = db.getUserHomewFlag(event.user_id)
    Schedule_flag = db.getUserSchedFlag(event.user_id)
    addHomework_flag = db.getUserAddHomewFlag(event.user_id)
    delHomework_flag = db.getUserDelHomewFlag(event.user_id)
    editHomework_flag = db.getUserEditHomewFlag(event.user_id)
    #
    if msg == 'Домашнее задание':
        db.changeUserHomewFlag(event.user_id, True)
        show_weekdays(event, db)
    elif msg == 'Расписание':
        db.changeUserSchedFlag(event.user_id, True)
        show_weekdays(event, db)
    elif msg == 'На сегодня' or msg == 'На завтра':
        operation_today_or_tomorrow(event, db)
    elif msg in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']:
        operations_with_weekdays(event, db, msg)
    elif msg == 'В главное меню':
        if Schedule_flag == True:
            db.changeUserSchedFlag(event.user_id, False)
        elif Homework_flag == True:
            db.changeUserHomewFlag(event.user_id, False)
        elif addHomework_flag == True:
            db.del_HomeworkObjectFromStack(event.user_id)
            db.changeUserAddHomewFlag(event.user_id, False)
        elif delHomework_flag == True:
            db.del_HomeworkObjectFromStack(event.user_id)
            db.changeUserDelHomewFlag(event.user_id, False)
        write_msg_withKeyboard(
            event.user_id, 'Главное меню', get_main_menu_keyboard(event))
    elif msg == 'На неделю':
        if Homework_flag == True:
            homework_on_week_menu()
    elif msg == 'На эту':
        get_homework_on_week(db, 0)
        db.changeUserHomewFlag(event.user_id, False)
    elif msg == 'На следующую':
        get_homework_on_week(db, 1)
        db.changeUserHomewFlag(event.user_id, False)
    elif msg == 'Указать число':
        if Homework_flag or addHomework_flag == True:
            set_date()
    elif msg == 'Редактирование':
        if user_is_admin_check(event) == True:
            editing()
    elif msg == 'Добавить домашнее задание':
        if user_is_admin_check(event) == True:
            db.changeUserAddHomewFlag(event.user_id, True)
            show_weekdays(event, db)
    elif msg == 'Редактировать домашнее задание':
        if user_is_admin_check(event) == True:
            db.changeUserEditHomewFlag(event.user_id, True)
            set_date()
    elif msg == 'Удаление домашнего задания':
        if user_is_admin_check(event) == True:
            db.changeUserDelHomewFlag(event.user_id, True)
            set_date()
    elif msg == 'Отмена':
        if addHomework_flag == True:
            db.del_HomeworkObjectFromStack(event.user_id)
            db.changeUserAddHomewFlag(event.user_id, False)
            db.changeUserStepCode(event.user_id, 0)
        elif delHomework_flag == True:
            db.del_HomeworkObjectFromStack(event.user_id)
            db.changeUserDelHomewFlag(event.user_id, False)
            db.changeUserStepCode(event.user_id, 0)
        elif Homework_flag == True:
            db.del_HomeworkObjectFromStack(event.user_id)
            db.changeUserHomewFlag(event.user_id, False)
            db.changeUserStepCode(event.user_id, 0)
        elif editHomework_flag == True:
            db.del_HomeworkObjectFromStack(event.user_id)
            db.changeUserStepCode(event.user_id, 0)
            db.changeUserEditHomewFlag(event.user_id, False)
        write_msg_withKeyboard(
            event.user_id, 'Главное меню', get_main_menu_keyboard(event))
    elif msg == 'Начать':
        write_msg_withKeyboard(
            event.user_id, 'Главное меню', get_main_menu_keyboard(event))
    else:
        different_operation(event, db, msg)
    db.close()


if __name__ == '__main__':
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
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                user_processing(event)
                msg = event.text
                check_command(event, msg)
