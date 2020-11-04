import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
#
from bd_direct import bdDirect
from directHomework import Homework
import config
import datetime
#
vk_session = vk_api.VkApi(token=config.token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
#
Homework_flag = False
schedule_flag = False
addHomework_flag = False
delHomework_flag = False
#
Homework = Homework()
step_code = 0
#


def write_msg(user_id, message):
    vk_session.method('messages.send', {
                      'user_id': user_id, 'message': str(message), 'random_id': 0})


def write_msg_withKeyboard(user_id, message, keyboard):
    vk_session.method('messages.send', {'user_id': user_id, 'message': str(
        message), 'random_id': 0, 'keyboard': keyboard.get_keyboard()})


def mainMenu(event):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Расписание', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Домашнее задание', color=VkKeyboardColor.POSITIVE)
    #
    if userIsAdmin(event) == True:
        keyboard.add_line()
        keyboard.add_button(
            'Редактирование', color=VkKeyboardColor.SECONDARY)
    #
    keyboard.add_line()
    keyboard.add_button('О боте', color=VkKeyboardColor.SECONDARY)
    write_msg_withKeyboard(event.user_id, 'Главное меню', keyboard)


def userIsAdmin(event):
    adminsList = getAdminList()
    rowcount = len(adminsList)
    row = 0
    userIsAdmin = False
    while row < rowcount:
        if event.user_id == adminsList[row][0]:
            userIsAdmin = True
            break
        row = row + 1
    return userIsAdmin


def getAdminList():
    db = bdDirect('Data Base/db.db')
    admins = db.get_admins()
    db.close()
    return admins


def ShowWeekdays():
    global Homework_flag
    #
    keyboard = VkKeyboard(one_time=True)
    if schedule_flag == True or Homework_flag == True:
        keyboard.add_button('На сегодня', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('На завтра', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
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
    #
    write_msg_withKeyboard(event.user_id, 'Выберите день недели', keyboard)


def AboutText():
    msg = 'Бот разработан @exodus_outcome (Максимом Ждановым)'
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def ScheduleOrOperHomework(msg):
    global addHomework_flag
    global schedule_flag
    global Homework_flag
    global delHomework_flag
    global step_code
    #
    if schedule_flag == True:
        schedule(msg)
        schedule_flag = False
    elif Homework_flag == True:
        homework(msg)
        Homework_flag = False
    elif addHomework_flag == True or delHomework_flag == True:
        Homework.setWeekday(msg)
        step_code = step_code + 1
        setLesson()


def Accusative(weekday):
    if weekday == 'Среда':
        return 'Среду'
    if weekday == 'Пятница':
        return 'Пятницу'
    if weekday == 'Суббота':
        return 'Субботу'
    else:
        return weekday


def schedule(weekday):
    db = bdDirect('Data Base/db.db')
    lesson = db.get_Lesson(weekday)
    db.close()
    #
    listLessons = []
    rowcount = len(lesson)
    row = 0
    while row < rowcount:
        start_time = lesson[row][2]
        end_time = lesson[row][3]
        lesson_name = lesson[row][4]
        cabinet = lesson[row][5]
        msg = str('🔹 ' + start_time + '-' + end_time +
                  ' ' + lesson_name + ' 📚 ' + str(cabinet))
        listLessons.append(msg)
        row = row + 1
    msg = '📝 Расписание уроков на ' + Accusative(weekday) + ':'
    for row in listLessons:
        msg = msg + '\n' + row
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def homework(weekday):
    db = bdDirect('Data Base/db.db')
    homework_tasks = db.get_Homework(weekday)
    db.close()
    #
    rowcount = len(homework_tasks)
    #
    if rowcount > 0:
        listHomework = []
        row = 0
        while row < rowcount:
            lesson_name = homework_tasks[row][0]
            task = homework_tasks[row][1]
            msg = str('♦ ' + lesson_name + ' - ' + task)
            listHomework.append(msg)
            row = row + 1
        msg = 'Домашнее задание на ' + Accusative(weekday) + ':'
        for rows in listHomework:
            msg = msg + '\n' + rows
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
        write_msg_withKeyboard(event.user_id, msg, keyboard)
    else:
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
        msg = 'Домашнего задания на ' + Accusative(weekday) + ' нет!'
        write_msg_withKeyboard(event.user_id, msg, keyboard)


def editing():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Добавить домашнее задание',
                        color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Удалить домашнее задание',
                        color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def add_homework():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Указать число',
                        color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Указать день недели',
                        color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Отмена', color=VkKeyboardColor.POSITIVE)
    #
    msg = 'Выберите вариант указания даты сдачи домашнего задания.'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def del_homework():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Указать число',
                        color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Отмена', color=VkKeyboardColor.POSITIVE)
    #
    msg = 'Выберите вариант указания даты для домашнего задания, которое хотите удалить'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def setDate():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Отмена', color=VkKeyboardColor.POSITIVE)
    msg = 'Напишите число в формате (День).(Месяц).(Год). Например 03.11.2018'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def setLesson():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Отмена', color=VkKeyboardColor.POSITIVE)
    msg = 'Напишите название урока'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def setTask():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Отмена', color=VkKeyboardColor.POSITIVE)
    msg = 'Напишите все задачи'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def setHomework():
    date = Homework.getDate()
    weekDay = Homework.getWeekday()
    lesson = Homework.getLesson()
    task = Homework.getTask()
    #
    db = bdDirect('Data Base/db.db')
    db.add_Homework(date, weekDay, lesson, task)
    db.close()
    #
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
    msg = 'Домашнее задание добавлено!'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def delHomework():
    date = Homework.getDate()
    lesson = Homework.getLesson()
    #
    db = bdDirect('Data Base/db.db')
    db.del_Homework(date, lesson)
    db.close()
    #
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
    msg = 'Домашнее задание удалено!'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def commandDirect(event, msg):
    global Homework_flag
    global schedule_flag
    global addHomework_flag
    global delHomework_flag
    global step_code
    global Homework
    #
    if msg == 'Start':
        mainMenu(event)
    elif msg == 'В главное меню':
        mainMenu(event)
    elif msg == 'Расписание':
        schedule_flag = True
        ShowWeekdays()
    elif msg == 'Домашнее задание':
        Homework_flag = True
        ShowWeekdays()
    #
    elif msg == 'На сегодня' or msg == 'На завтра':
        if schedule_flag == True or Homework_flag == True:
            now = datetime.datetime.now()
            idWeekday = now.weekday()
            weekdays = ['Понедельник', 'Вторник', 'Среда',
                        'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
            if schedule_flag == True:
                ##
                schedule_flag = False
                if msg == 'На сегодня':
                    schedule(weekdays[idWeekday])
                elif msg == 'На завтра':
                    schedule(weekdays[idWeekday + 1])
                ##
            elif Homework_flag == True:
                ##
                Homework_flag = False
                if msg == 'На сегодня':
                    homework(weekdays[idWeekday])
                elif msg == 'На завтра':
                    homework(weekdays[idWeekday + 1])
                ##
    #
    elif msg == 'Понедельник':
        ScheduleOrOperHomework(msg)
    elif msg == 'Вторник':
        ScheduleOrOperHomework(msg)
    elif msg == 'Среда':
        ScheduleOrOperHomework(msg)
    elif msg == 'Четверг':
        ScheduleOrOperHomework(msg)
    elif msg == 'Пятница':
        ScheduleOrOperHomework(msg)
    elif msg == 'Суббота':
        ScheduleOrOperHomework(msg)
    elif msg == 'Редактирование':
        if userIsAdmin(event) == True:
            editing()
    elif msg == 'Добавить домашнее задание':
        if userIsAdmin(event) == True:
            addHomework_flag = True
            add_homework()
    elif msg == 'Удалить домашнее задание':
        if userIsAdmin(event) == True:
            delHomework_flag = True
            del_homework()
    elif msg == 'Указать число':
        if userIsAdmin(event) == True:
            if addHomework_flag == True:
                setDate()
            if delHomework_flag == True:
                setDate()
    elif msg == 'Указать день недели':
        if userIsAdmin(event) == True:
            if addHomework_flag == True:
                ShowWeekdays()
    #
    elif msg == 'Отмена':
        if addHomework_flag == True or delHomework_flag == True:
            Homework.clearStack()
            step_code = 0
            addHomework_flag = False
            delHomework_flag = False
            mainMenu(event)
    #
    elif msg == 'О боте':
        AboutText()
    else:
        if addHomework_flag == True or delHomework_flag == True:
            if step_code == 0:
                Homework.setDate(msg)
                step_code = step_code + 1
                setLesson()
            elif step_code == 1:
                Homework.setLesson(msg)
                if addHomework_flag == True:
                    step_code = step_code + 1
                    setTask()
                elif delHomework_flag == True:
                    delHomework()
                    step_code = 0
                    delHomework_flag = False
                    Homework.clearStack()
            elif step_code == 2:
                Homework.setTask(msg)
                setHomework()
                step_code = 0
                addHomework_flag = False
                Homework.clearStack()


if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = event.text
                commandDirect(event, msg)
