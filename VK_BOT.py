#
import re
import config
import datetime
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from request_db import requestDB
from homework_opers import Homework
from check_InputData import *
import config_pars
#
vk_session = vk_api.VkApi(token=config.token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
Homework = Homework()
users = None
#


def showWeekdays(event, db):
    Homework_flag = db.getUserHomewFlag(event.user_id)
    Schedule_flag = db.getUserSchedFlag(event.user_id)
    addHomework_flag = db.getUserAddHomewFlag(event.user_id)
    #
    if Homework_flag or addHomework_flag == True:
        msg = 'Выберите день недели или укажите дату...'
    else:
        msg = 'Выберите день недели...'
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


def operWithWeekdays(event, db, msg):
    addHomework_flag = db.getUserAddHomewFlag(event.user_id)
    Homework_flag = db.getUserHomewFlag(event.user_id)
    Schedule_flag = db.getUserSchedFlag(event.user_id)
    delHomework_flag = db.getUserDelHomewFlag(event.user_id)
    step_code = db.getUserStepCode(event.user_id)
    #
    if Homework_flag == True:
        sendHomework(event, db, msg)
        db.changeUserHomewFlag(event.user_id, False)
    elif Schedule_flag == True:
        sendSchedule(db, msg)
        db.changeUserSchedFlag(event.user_id, False)
    elif addHomework_flag == True or delHomework_flag == True:
        Homework.set_Weekday(msg)
        db.changeUserStepCode(event.user_id, (step_code + 1))
        set_Lesson()


def operTodayOrTomorrow(event, db):
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
                sendHomework(event, db, weekdays[idWeekday], 1, True)
            elif msg == 'На завтра':
                if idWeekday == 6:
                    sendHomework(event, db, weekdays[0], 2)
                else:
                    sendHomework(event, db, weekdays[idWeekday + 1], 2)
            db.changeUserHomewFlag(event.user_id, False)
        elif Schedule_flag == True:
            db.changeUserSchedFlag(event.user_id, False)
            if msg == 'На сегодня':
                sendSchedule(db, weekdays[idWeekday])
            elif msg == 'На завтра':
                if idWeekday == 6:
                    sendSchedule(db, weekdays[0])
                else:
                    sendSchedule(db, weekdays[idWeekday + 1])
        elif addHomework_flag == True:
            if idWeekday == 6:
                Homework.set_Weekday(weekdays[0])
            else:
                Homework.set_Weekday(weekdays[idWeekday + 1])
            db.changeUserStepCode(event.user_id, 1)
            set_Lesson()


def accusative(weekday):
    if weekday == 'Среда':
        return 'Среду'
    elif weekday == 'Пятница':
        return 'Пятницу'
    elif weekday == 'Суббота':
        return 'Субботу'
    else:
        return weekday


def differentOperation(event, db, msg):
    Homework_flag = db.getUserHomewFlag(event.user_id)
    addHomework_flag = db.getUserAddHomewFlag(event.user_id)
    delHomework_flag = db.getUserDelHomewFlag(event.user_id)
    editHomework_flag = db.getUserEditHomewFlag(event.user_id)
    step_code = db.getUserStepCode(event.user_id)
    #
    if addHomework_flag or delHomework_flag or Homework_flag or editHomework_flag == True:  # or getLessonDate_flag
        # Date
        if step_code == 0:
            if Check_Date(msg) == True:
                Homework.set_Date(msg)
                if Homework_flag == True:
                    sendHomework(event, db, None, 3)
                    db.changeUserHomewFlag(event.user_id, False)
                elif addHomework_flag or delHomework_flag == True:
                    db.changeUserStepCode(event.user_id, 1)
                    set_Lesson()
                else:
                    db.changeUserStepCode(event.user_id, 1)
                    getEditCommand(event)
            else:
                msg = 'Ошибка даты: неверный формат.'
                write_msg(event.user_id, msg)
                set_Date()
        if userIsAdminCheck(event) == True:
            # Lesson
            if step_code == 1:
                if editHomework_flag == True:
                    editHomework(event, msg)
                    Homework.clear_Stack()
                    db.changeUserStepCode(event.user_id, 0)
                    db.changeUserEditHomewFlag(event.user_id, False)
                elif Check_Lesson(msg) == True:
                    if addHomework_flag == True:
                        Homework.set_Lesson(msg)
                        db.changeUserStepCode(event.user_id, 2)
                        set_Task()
                    elif delHomework_flag == True:
                        Homework.set_Lesson(msg)
                        db.changeUserStepCode(event.user_id, 0)
                        db.changeUserDelHomewFlag(event.user_id, False)
                        delete_Homework(db)
                        Homework.clear_Stack()
                else:
                    msg = 'Ошибка названия урока: длина не может превышать 16 символов.'
                    write_msg(event.user_id, msg)
                    set_Lesson()
            # Task
            elif step_code == 2:
                if Check_Tasks(msg) == True:
                    msg = msg.replace('''&quot;''', '''"''')
                    Homework.set_Task(msg)
                    db.changeUserStepCode(event.user_id, 0)
                    db.changeUserAddHomewFlag(event.user_id, False)
                    set_Homework(db)
                    Homework.clear_Stack()
                else:
                    msg = 'Ошибка задач: длина не может превышать 512 символов.'
                    write_msg(event.user_id, msg)
                    set_Task()
    else:
        msg = 'Данной команды не существует.'
        write_msg(event.user_id, msg)


def sendSchedule(db, weekday):
    if weekday == 'Воскресенье':
        msg = 'Уроки в воскресенье? Всё нормально? Лучше поспи, отдохни, хорошо покушай.'
        write_msg_withKeyboard(event.user_id, msg, get_MainMenuKeyboard(event))
        return
    #
    weekConfig = config_pars.getWeekConfig('Settings.ini')
    if getWeekdayId(weekday) >= datetime.datetime.now().weekday():
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
    msg = '📚 Расписание уроков на {0}:'.format(accusative(weekday))
    for row in listLessons:
        msg += '\n' + row
    write_msg_withKeyboard(event.user_id, msg, get_MainMenuKeyboard(event))


def getWeekdayId(weekday):
    weekdays = ['Понедельник', 'Вторник', 'Среда',
                'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    idWeekday = 0
    for w in weekdays:
        if w == weekday:
            return idWeekday
        else:
            idWeekday += 1


def sendHomework(event, db, weekday=None, mode=0, today=False):
    if weekday != None:
        if today == True:
            now = datetime.datetime.now().strftime('%d.%m.%Y')
            Homework.set_Date(str(now))
        else:
            Homework.get_DateByWeekday(weekday)
    else:
        Homework.set_Weekday()
        weekday = Homework.get_Weekday()
    date = Homework.get_Date()
    #
    date_type = datetime.datetime.strptime(date, '%d.%m.%Y')
    now = datetime.datetime.now()
    idNowWeekday = now.weekday()
    delt = now - date_type
    if int(delt.days) > idNowWeekday:
        msg = 'Вы пытаетесь посмотреть домашнее задание на давний срок. В главной базе данных хранятся все домашние \
               задания начиная с текущей недели. Чтобы всё-таки узнать нужное вам домашнее задание, обратитесь к \
               администратору - @3x0d2s(Максим Жданов).'
        Homework.clear_Stack()
        write_msg_withKeyboard(event.user_id, msg, get_MainMenuKeyboard(event))
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
                if checkNewLineInTaskText(task) == True:
                    msg = str('🔺 {0}:\n{1}'.format(lesson_name, task))
                else:
                    msg = str('🔺 {0}: {1}'.format(lesson_name, task))
                listHomework.append(msg)
            msg = '📝 Домашнее задание на {0} ({1}):'.format(
                accusative(weekday), date)
            for rows in listHomework:
                msg += '\n' + rows
        else:
            if mode == 0:
                if weekday == 'Понедельник' or weekday == 'Вторник' or weekday == 'Четверг':
                    msg = 'На ближайший {0} нет домашнего задания.'.format(
                        weekday.lower())
                else:
                    msg = 'На ближайшую {0} нет домашнего задания.'.format(
                        accusative(weekday).lower())
            elif mode == 1:
                msg = 'На сегодня нет домашнего задания.'
            elif mode == 2:
                msg = 'На завтра нет домашнего задания.'
            elif mode == 3:
                if weekday == 'Понедельник' or weekday == 'Вторник' or weekday == 'Четверг':
                    msg = 'На {0} {1} нет домашнего задания.'.format(
                        accusative(weekday).lower(), date)
    elif weekday == 'Воскресенье':
        msg = 'Домашнее задание на воскресенье? Совсем переучились?'
    Homework.clear_Stack()
    write_msg_withKeyboard(event.user_id, msg, get_MainMenuKeyboard(event))


def set_Homework(db):
    date = Homework.get_Date()
    weekDay = Homework.get_Weekday()
    lesson = Homework.get_Lesson()
    task = Homework.get_Task()
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
                event.user_id, msg, get_MainMenuKeyboard(event))
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


def delete_Homework(db):
    date = Homework.get_Date()
    lesson = Homework.get_Lesson()
    #
    if db.check_Homework(date, lesson) == True:
        db.del_Homework(date, lesson)
        db.close()
        msg = 'Домашнее задание удалено!'
        write_msg_withKeyboard(event.user_id, msg, get_MainMenuKeyboard(event))
    else:
        msg = 'Такого домашнего задания не существует.'
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Удаление домашнего задания',
                            color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
        write_msg_withKeyboard(event.user_id, msg, keyboard)


def editHomework(event, msg):
    pattern = re.compile('::')
    if pattern.findall(msg):
        result = ''
        сommand_parts = msg.split('::', maxsplit=1)
        lesson_h = сommand_parts[0]
        task_h = сommand_parts[1]
        #
        if len(lesson_h) == 0:
            result += 'Ошибка: вы не указали название урока.\n'
        if len(task_h) == 0:
            result += 'Ошибка: вы не указали измененное задание.\n'
        if Check_Lesson(lesson_h) == False:
            result += 'Ошибка названия урока: длина не может превышать 32 символа.\n'
        if Check_Tasks(task_h) == False:
            result += 'Ошибка текста задания: длина не может превышать 512 символов.\n'
        if result == '':
            date_h = Homework.get_Date()
            db = requestDB('Data Base/db.db')
            if db.check_Homework(date_h, lesson_h) == True:
                if task_h[0] == '\n':
                    task_h = task_h.replace('\n', '', 1)
                task_h = task_h.replace('''&quot;''', '''"''')
                db.editHomework(date_h, lesson_h, task_h)
                db.close()
                msg = 'Домашнее задание было отредактировано.'
            else:
                msg = 'Указанное домашнее задание не существует.'
        else:
            msg = result
    else:
        msg = 'Ошибка формата команды.'
    write_msg_withKeyboard(event.user_id, msg, get_MainMenuKeyboard(event))


def getHomeworkOnWeek(db, mode):
    ''' mode:
        0 - this week
        1 - next week'''
    allHomework = db.get_allHomework()
    #
    if len(allHomework) == 0:
        if mode == 0:
            output = 'Домашнее задание на эту неделю не было найдено.'
            write_msg_withKeyboard(event.user_id, output,
                                   get_MainMenuKeyboard(event))
        elif mode == 1:
            output = 'Домашнее задание на следующую неделю не было найдено.'
            write_msg_withKeyboard(event.user_id, output,
                                   get_MainMenuKeyboard(event))
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
                weekday_h = Homework.get_WeekdayByDate(date)
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
                        if checkNewLineInTaskText(task) == True:
                            output += str('🔺 {0} на {1}:\n{2}\n'.format(
                                homew[1], accusative(homew[2]).lower(), homew[3]))
                        else:
                            output += str('🔺 {0} на {1}: {2}\n'.format(
                                homew[1], accusative(homew[2]).lower(), homew[3]))
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
                weekday_h = Homework.get_WeekdayByDate(date)
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
                        if checkNewLineInTaskText(task) == True:
                            output += str('🔺 {0} на {1}:\n{2}\n'.format(
                                homew[1], accusative(homew[2]).lower(), homew[3]))
                        else:
                            output += str('🔺 {0} на {1}: {2}\n'.format(
                                homew[1], accusative(homew[2]).lower(), homew[3]))
                        homew_goto.append(homew)
    write_msg_withKeyboard(event.user_id, output, get_MainMenuKeyboard(event))


def checkNewLineInTaskText(task):
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


def get_MainMenuKeyboard(event):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Расписание', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Домашнее задание', color=VkKeyboardColor.POSITIVE)
    if userIsAdminCheck(event) == True:
        keyboard.add_line()
        keyboard.add_button(
            'Редактирование', color=VkKeyboardColor.SECONDARY)
    return keyboard


def get_EditingKeyboard():
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


def getUsers(db):
    global users
    users = db.get_users()


def checkUser(event):
    db = requestDB('Data Base/db.db')
    if len(users) != 0:
        newUser = True
        user_id = event.user_id
        for user in range(len(users)):
            if user_id == users[user][0]:
                newUser = False
                break
        if newUser == True:
            db.add_user(event.user_id)
            getUsers(db)
    else:
        db.add_user(event.user_id)
        getUsers(db)
    db.close()


def userIsAdminCheck(event):
    user_id = event.user_id
    for user in range(len(users)):
        if user_id == users[user][0]:
            return users[user][1]  # True or False


def HomeworkOnWeekMenu():
    msg = 'Выберите неделю...'
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Эта', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Следующая', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def getEditCommand(event):
    msg = 'Введите команду в формате (Название урока)::(Обновленное задание). Например Алгебра::Решить номера 150-155'
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def editing():
    msg = 'Выберите действие...'
    write_msg_withKeyboard(event.user_id, msg, get_EditingKeyboard())


def set_Date():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    msg = 'Введите число в формате (День).(Месяц).(Год). Например 03.11.2018'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def set_Lesson():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    msg = 'Введите название урока...'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def set_Task():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    msg = 'Введите все задачи...'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def checkCommand(event, msg):
    db = requestDB('Data Base/db.db')
    Homework_flag = db.getUserHomewFlag(event.user_id)
    Schedule_flag = db.getUserSchedFlag(event.user_id)
    addHomework_flag = db.getUserAddHomewFlag(event.user_id)
    delHomework_flag = db.getUserDelHomewFlag(event.user_id)
    editHomework_flag = db.getUserEditHomewFlag(event.user_id)
    #getLessDate_flag = db.getUserGetLessDateFlag(event.user_id)
    #
    if msg == 'Домашнее задание':
        db.changeUserHomewFlag(event.user_id, True)
        showWeekdays(event, db)
    elif msg == 'Расписание':
        db.changeUserSchedFlag(event.user_id, True)
        showWeekdays(event, db)
    elif msg == 'На сегодня' or msg == 'На завтра':
        operTodayOrTomorrow(event, db)
    elif msg in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']:
        operWithWeekdays(event, db, msg)
    elif msg == 'В главное меню':
        if Schedule_flag == True:
            db.changeUserSchedFlag(event.user_id, False)
        elif Homework_flag == True:
            db.changeUserHomewFlag(event.user_id, False)
        elif addHomework_flag == True:
            Homework.clear_Stack()
            db.changeUserAddHomewFlag(event.user_id, False)
        elif delHomework_flag == True:
            Homework.clear_Stack()
            db.changeUserDelHomewFlag(event.user_id, False)
        write_msg_withKeyboard(
            event.user_id, 'Главное меню', get_MainMenuKeyboard(event))
    elif msg == 'На неделю':
        if Homework_flag == True:
            HomeworkOnWeekMenu()
    elif msg == 'Эта':
        getHomeworkOnWeek(db, 0)
        db.changeUserHomewFlag(event.user_id, False)
    elif msg == 'Следующая':
        getHomeworkOnWeek(db, 1)
        db.changeUserHomewFlag(event.user_id, False)
    elif msg == 'Указать число':
        if Homework_flag or addHomework_flag == True:
            set_Date()
    elif msg == 'Редактирование':
        if userIsAdminCheck(event) == True:
            editing()
    elif msg == 'Добавить домашнее задание':
        if userIsAdminCheck(event) == True:
            db.changeUserAddHomewFlag(event.user_id, True)
            showWeekdays(event, db)
    elif msg == 'Редактировать домашнее задание':
        if userIsAdminCheck(event) == True:
            db.changeUserEditHomewFlag(event.user_id, True)
            set_Date()
    elif msg == 'Удаление домашнего задания':
        if userIsAdminCheck(event) == True:
            db.changeUserDelHomewFlag(event.user_id, True)
            set_Date()
    elif msg == 'Отмена':
        if addHomework_flag == True:
            Homework.clear_Stack()
            db.changeUserAddHomewFlag(event.user_id, False)
            db.changeUserStepCode(event.user_id, 0)
        elif delHomework_flag == True:
            Homework.clear_Stack()
            db.changeUserDelHomewFlag(event.user_id, False)
            db.changeUserStepCode(event.user_id, 0)
        elif Homework_flag == True:
            Homework.clear_Stack()
            db.changeUserHomewFlag(event.user_id, False)
            db.changeUserStepCode(event.user_id, 0)
        elif editHomework_flag == True:
            Homework.clear_Stack()
            db.changeUserStepCode(event.user_id, 0)
            db.changeUserEditHomewFlag(event.user_id, False)
        write_msg_withKeyboard(
            event.user_id, 'Главное меню', get_MainMenuKeyboard(event))
    elif msg == 'Начать':
        write_msg_withKeyboard(
            event.user_id, 'Главное меню', get_MainMenuKeyboard(event))
    else:
        differentOperation(event, db, msg)
    db.close()


if __name__ == '__main__':
    db = requestDB('Data Base/db.db')
    getUsers(db)
    db.close()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                checkUser(event)
                msg = event.text
                checkCommand(event, msg)
