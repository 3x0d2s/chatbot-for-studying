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


def showWeekdays(event):
    db = requestDB('Data Base/db.db')
    Homework_flag = db.getUserHomewFlag(event.user_id)
    Schedule_flag = db.getUserSchedFlag(event.user_id)
    addHomework_flag = db.getUserAddHomewFlag(event.user_id)
    db.close()
    #
    if Homework_flag or addHomework_flag == True:
        msg = 'Выберите день недели или укажите дату...'
    else:
        msg = 'Выберите день недели...'
    #
    keyboard = VkKeyboard(one_time=False)
    if Homework_flag == True:
        keyboard.add_button('Указать число', color=VkKeyboardColor.POSITIVE)
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


def operWithWeekdays(event, msg):
    db = requestDB('Data Base/db.db')
    addHomework_flag = db.getUserAddHomewFlag(event.user_id)
    Homework_flag = db.getUserHomewFlag(event.user_id)
    Schedule_flag = db.getUserSchedFlag(event.user_id)
    delHomework_flag = db.getUserDelHomewFlag(event.user_id)
    step_code = db.getUserStepCode(event.user_id)
    #
    if Homework_flag == True:
        sendHomework(event, msg)
        db.changeUserHomewFlag(event.user_id, False)
    elif Schedule_flag == True:
        sendSchedule(msg)
        db.changeUserSchedFlag(event.user_id, False)
    elif addHomework_flag == True or delHomework_flag == True:
        Homework.set_Weekday(msg)
        db.changeUserStepCode(event.user_id, (step_code + 1))
        set_Lesson()
    db.close()


def operTodayOrTomorrow(event):
    db = requestDB('Data Base/db.db')
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
                sendHomework(event, weekdays[idWeekday], 1, True)
            elif msg == 'На завтра':
                if idWeekday == 6:
                    sendHomework(event, weekdays[0], 2)
                else:
                    sendHomework(event, weekdays[idWeekday + 1], 2)
        elif Schedule_flag == True:
            db.changeUserSchedFlag(event.user_id, False)
            if msg == 'На сегодня':
                sendSchedule(weekdays[idWeekday])
            elif msg == 'На завтра':
                if idWeekday == 6:
                    sendSchedule(weekdays[0])
                else:
                    sendSchedule(weekdays[idWeekday + 1])
        elif addHomework_flag == True:
            if idWeekday == 6:
                Homework.set_Weekday(weekdays[0])
            else:
                Homework.set_Weekday(weekdays[idWeekday + 1])
            db.changeUserStepCode(event.user_id, 1)
            set_Lesson()
    db.close()


def accusative(weekday):
    if weekday == 'Среда':
        return 'Среду'
    elif weekday == 'Пятница':
        return 'Пятницу'
    elif weekday == 'Суббота':
        return 'Субботу'
    else:
        return weekday


def differentOperation(event, msg):
    db = requestDB('Data Base/db.db')
    Homework_flag = db.getUserHomewFlag(event.user_id)
    addHomework_flag = db.getUserAddHomewFlag(event.user_id)
    delHomework_flag = db.getUserDelHomewFlag(event.user_id)
    getLessonDate_flag = db.getUserGetLessDateFlag(event.user_id)
    editHomework_flag = db.getUserEditHomewFlag(event.user_id)
    step_code = db.getUserStepCode(event.user_id)
    #
    if addHomework_flag or delHomework_flag or Homework_flag or getLessonDate_flag or editHomework_flag == True:
        # Date
        if step_code == 0:
            if Check_Date(msg) == True:
                Homework.set_Date(msg)
                if Homework_flag == True:
                    sendHomework(event, None, 3)
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
                        delete_Homework()
                        Homework.clear_Stack()
                    elif getLessonDate_flag == True:
                        msg = get_DateByLesson(msg)
                        db.changeUserStepCode(event.user_id, 0)
                        db.changeUserGetLessDateFlag(event.user_id, False)
                        write_msg_withKeyboard(
                            event.user_id, msg, get_EditingKeyboard())
                else:
                    msg = 'Ошибка названия урока: длина не может превышать 16 символов.'
                    write_msg(event.user_id, msg)
                    set_Lesson()
            # Task
            elif step_code == 2:
                if Check_Tasks(msg) == True:
                    Homework.set_Task(msg)
                    db.changeUserStepCode(event.user_id, 0)
                    db.changeUserAddHomewFlag(event.user_id, False)
                    set_Homework()
                    Homework.clear_Stack()
                else:
                    msg = 'Ошибка задач: длина не может превышать 512 символов.'
                    write_msg(event.user_id, msg)
                    set_Task()
    else:
        msg = 'Данной команды не существует.'
        write_msg(event.user_id, msg)
    db.close()


def sendSchedule(weekday):
    if weekday == 'Воскресенье':
        msg = 'Уроки в воскресенье? Всё нормально? Лучше поспи, отдохни, хорошо покушай.'
        write_msg_withKeyboard(event.user_id, msg, get_MainMenuKeyboard(event))
        return
    #
    weekConfig = config_pars.getWeekConfig('Settings.ini')
    db = requestDB('Data Base/db.db')
    lesson = db.get_Lesson(weekday, weekConfig)
    db.close()
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
    msg = '📚 Расписание уроков на ' + accusative(weekday) + ':'
    for row in listLessons:
        msg = msg + '\n' + row
    write_msg_withKeyboard(event.user_id, msg, get_MainMenuKeyboard(event))


def sendHomework(event, weekday=None, mode=0, today=False):
    db = requestDB('Data Base/db.db')
    if weekday != None:
        if today == True:
            now = datetime.datetime.now().strftime('%d.%m.%Y')
            Homework.set_Date(str(now))
        else:
            Homework.get_DateByWeekday(weekday)
    else:
        Homework.set_Weekday()
        weekday = Homework.get_Weekday()
    #
    date = Homework.get_Date()
    if weekday != 'Воскресенье':
        homework_tasks = db.get_Homework(date)
        rowcount = len(homework_tasks)
        if rowcount > 0:
            listHomework = []
            for row in range(rowcount):
                lesson_name = homework_tasks[row][0]
                task = homework_tasks[row][1]
                if checkNewLineInTaskText(task) == True:
                    msg = str('♦ ' + lesson_name + ':\n' + task)
                else:
                    msg = str('♦ ' + lesson_name + ': ' + task)
                listHomework.append(msg)
            msg = '📝 Домашнее задание на ' + \
                accusative(weekday) + ' (' + date + ')' + ':'
            for rows in listHomework:
                msg = msg + '\n' + rows
        else:
            if mode == 0:
                if weekday == 'Понедельник' or weekday == 'Вторник' or weekday == 'Четверг':
                    msg = 'На ближайший ' + weekday.lower() + ' нет домашнего задания.'
                else:
                    msg = 'На ближайшую ' + \
                        accusative(weekday).lower() + ' нет домашнего задания.'
            elif mode == 1:
                msg = 'На сегодня нет домашнего задания.'
            elif mode == 2:
                msg = 'На завтра нет домашнего задания.'
            elif mode == 3:
                if weekday == 'Понедельник' or weekday == 'Вторник' or weekday == 'Четверг':
                    msg = 'На ' + \
                        accusative(weekday).lower() + ' ' + \
                        date + ' нет домашнего задания.'
                else:
                    msg = 'На ' + \
                        accusative(weekday).lower() + ' ' + \
                        date + ' нет домашнего задания.'
    elif weekday == 'Воскресенье':
        msg = 'Домашнее задание на воскресенье? Совсем переучились?'
    Homework.clear_Stack()
    db.changeUserHomewFlag(event.user_id, False)
    db.close()
    write_msg_withKeyboard(event.user_id, msg, get_MainMenuKeyboard(event))


def set_Homework():
    date = Homework.get_Date()
    weekDay = Homework.get_Weekday()
    lesson = Homework.get_Lesson()
    task = Homework.get_Task()
    #
    db = requestDB('Data Base/db.db')
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
    db.close()


def delete_Homework():
    date = Homework.get_Date()
    lesson = Homework.get_Lesson()
    #
    db = requestDB('Data Base/db.db')
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
        result = None
        сommand_parts = msg.split('::')
        lesson_h = сommand_parts[0]
        task_h = сommand_parts[1]
        if Check_Lesson(lesson_h) == False:
            result = 'Ошибка названия урока: длина не может превышать 32 символа.\n'
        if Check_Tasks(task_h) == False:
            result += 'Ошибка текста задания: длина не может превышать 512 символов.\n'
        if result == None:
            date_h = Homework.get_Date()
            db = requestDB('Data Base/db.db')
            if db.check_Homework(date_h, lesson_h) == True:
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


def checkNewLineInTaskText(task):
    pattern = re.compile(r'\n')
    if pattern.findall(task):
        return True
    return False


def get_DateByLesson(lesson):
    weekConfig = config_pars.getWeekConfig('Settings.ini')
    db = requestDB('Data Base/db.db')
    lessons = db.get_allLesson(weekConfig)
    db.close()
    #
    lesson = msg
    main_list = []
    for step in range(len(lessons)):
        if lesson == lessons[step][1]:  # 0 - weekday 1 - lesson
            weekday = lessons[step][0]
            date = datetime.datetime.strptime(
                Homework.get_DateByWeekday(weekday, 1), '%d.%m.%Y')
            main_list.append([date, weekday])
    if len(main_list) > 0:
        now = datetime.datetime.now().replace(
            hour=0, second=0, microsecond=0, minute=0)
        idThisWeekday = now.weekday()
        #
        for step in main_list:
            idStepLesson = step[0].weekday()
            if idStepLesson > idThisWeekday:
                if step[1] == 'Вторник':
                    return lesson + ' будет во ' + accusative(step[1]) + ' (' + str(step[0].strftime('%d.%m.%Y')) + ')'
                else:
                    return lesson + ' будет в ' + accusative(step[1]) + ' (' + str(step[0].strftime('%d.%m.%Y')) + ')'
        if main_list[0][1] == 'Вторник':
            return lesson + ' будет во ' + accusative(main_list[0][1]) + ' (' + str(main_list[0][0].strftime('%d.%m.%Y')) + ')'
        else:
            return lesson + ' будет в ' + accusative(main_list[0][1]) + ' (' + str(main_list[0][0].strftime('%d.%m.%Y')) + ')'
    else:
        return 'Такой урок не был найден.'


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
    keyboard.add_button('Когда следующий урок?',
                        color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
    return keyboard


def getUsers():
    global users
    db = requestDB('Data Base/db.db')
    users = db.get_users()
    db.close()


def checkUser(event):
    if len(users) != 0:
        newUser = True
        user_id = event.user_id
        for user in range(len(users)):
            if user_id == users[user][0]:
                newUser = False
                break
        if newUser == True:
            db = requestDB('Data Base/db.db')
            db.add_user(event.user_id)
            db.close()
            getUsers()
    else:
        db = requestDB('Data Base/db.db')
        db.add_user(event.user_id)
        db.close()
        getUsers()


def userIsAdminCheck(event):
    user_id = event.user_id
    for user in range(len(users)):
        if user_id == users[user][0]:
            return users[user][1]  # True or False


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
    getLessDate_flag = db.getUserGetLessDateFlag(event.user_id)
    editHomework_flag = db.getUserEditHomewFlag(event.user_id)
    #
    if msg == 'Домашнее задание':
        db.changeUserHomewFlag(event.user_id, True)
        showWeekdays(event)
    elif msg == 'Расписание':
        db.changeUserSchedFlag(event.user_id, True)
        showWeekdays(event)
    elif msg == 'На сегодня' or msg == 'На завтра':
        operTodayOrTomorrow(event)
    elif (msg == 'Понедельник' or msg == 'Вторник' or msg == 'Среда'
          or msg == 'Четверг' or msg == 'Пятница' or msg == 'Суббота'):
        operWithWeekdays(event, msg)
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
    elif msg == 'Указать число':
        if Homework_flag or addHomework_flag == True:
            set_Date()
    elif msg == 'Редактирование':
        if userIsAdminCheck(event) == True:
            editing()
    elif msg == 'Добавить домашнее задание':
        if userIsAdminCheck(event) == True:
            db.changeUserAddHomewFlag(event.user_id, True)
            showWeekdays(event)
    elif msg == 'Редактировать домашнее задание':
        if userIsAdminCheck(event) == True:
            db.changeUserEditHomewFlag(event.user_id, True)
            set_Date()
    elif msg == 'Удаление домашнего задания':
        if userIsAdminCheck(event) == True:
            db.changeUserDelHomewFlag(event.user_id, True)
            set_Date()
    elif msg == 'Когда следующий урок?':
        if userIsAdminCheck(event) == True:
            db.changeUserGetLessDateFlag(event.user_id, True)
            db.changeUserStepCode(event.user_id, 1)
            set_Lesson()
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
        elif getLessDate_flag == True:
            db.changeUserGetLessDateFlag(event.user_id, False)
            db.changeUserStepCode(event.user_id, 0)
        write_msg_withKeyboard(
            event.user_id, 'Главное меню', get_MainMenuKeyboard(event))
    elif msg == 'Начать':
        write_msg_withKeyboard(
            event.user_id, 'Главное меню', get_MainMenuKeyboard(event))
    else:
        differentOperation(event, msg)
    db.close()


if __name__ == '__main__':
    getUsers()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                checkUser(event)
                msg = event.text
                checkCommand(event, msg)
