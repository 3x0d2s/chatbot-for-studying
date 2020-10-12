import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
#
from bd_schedule_direct import scheduleDirect
from setHomework import addHomework
import config
#
vk_session = vk_api.VkApi(token=config.token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
#
homework_flag = False
schedule_flag = False
addHomework_flag = False
#
addHomework = addHomework()
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
    db = scheduleDirect('Data Base/db.db')
    admins = db.get_admins()
    db.close()
    return admins


def ShowWeekdays():
    keyboard = VkKeyboard(one_time=True)
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
    msg = 'Бот разработан Максимом Ждановым - vk.com/exodus_outcome'
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def ScheduleOrHomework(msg):
    global homework_flag
    global schedule_flag
    global addHomework_flag
    global step_code
    #
    if schedule_flag == True:
        schedule(msg)
        schedule_flag = False
    elif homework_flag == True:
        homework(msg)
        homework_flag = False
    elif addHomework_flag == True:
        addHomework.setWeekday(msg)
        step_code = step_code + 1
        setLesson()


def schedule(weekday):
    db = scheduleDirect('Data Base/db.db')
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
        msg = str(str(row + 1) + ') ' + lesson_name + ' ' +
                  start_time + '-' + end_time + ' | ' + str(cabinet))
        listLessons.append(msg)
        row = row + 1
    msg = 'Расписание уроков на ' + weekday + ':'
    for row in listLessons:
        msg = msg + '\n' + row
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def homework(weekday):
    db = scheduleDirect('Data Base/db.db')
    homework_tasks = db.get_Homework(weekday)
    db.close()
    #
    listHomework = []
    rowcount = len(homework_tasks)
    row = 0
    while row < rowcount:
        lesson_name = homework_tasks[row][0]
        task = homework_tasks[row][1]
        msg = str(str(row + 1) + ') ' + lesson_name + ' - ' + task)
        listHomework.append(msg)
        row = row + 1
    msg = 'Домашнее задание на ' + weekday + ':'
    for row in listHomework:
        msg = msg + '\n' + row
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def editing():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Добавить домашнее задание',
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


def setDate():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Отмена', color=VkKeyboardColor.POSITIVE)
    #
    msg = 'Напишите число в формате (День).(Месяц).(Год). Например 03.11.2018'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def setLesson():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Отмена', color=VkKeyboardColor.POSITIVE)
    #
    msg = 'Напишите название урока'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def setTask():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Отмена', color=VkKeyboardColor.POSITIVE)
    #
    msg = 'Напишите все задачи'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def setHomework():
    date = addHomework.getDate()
    weekDay = addHomework.getWeekday()
    lesson = addHomework.getLesson()
    task = addHomework.getTask()
    #
    db = scheduleDirect('Data Base/db.db')
    db.add_Homework(date, weekDay, lesson, task)
    db.close()
    #
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
    msg = 'Домашнее задание добавлено!'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def commandDirect(event, msg):
    global homework_flag
    global schedule_flag
    global addHomework_flag
    global step_code
    global addHomework
    #
    if msg == 'Start':
        mainMenu(event)
    elif msg == 'В главное меню':
        mainMenu(event)
    elif msg == 'Расписание':
        schedule_flag = True
        ShowWeekdays()
    elif msg == 'Домашнее задание':
        homework_flag = True
        ShowWeekdays()
    elif msg == 'Понедельник':
        ScheduleOrHomework(msg)
    elif msg == 'Вторник':
        ScheduleOrHomework(msg)
    elif msg == 'Среда ':
        ScheduleOrHomework(msg)
    elif msg == 'Четверг':
        ScheduleOrHomework(msg)
    elif msg == 'Пятница':
        ScheduleOrHomework(msg)
    elif msg == 'Суббота':
        ScheduleOrHomework(msg)
    elif msg == 'Редактирование':
        if userIsAdmin(event) == True:
            editing()
    elif msg == 'Добавить домашнее задание':
        if userIsAdmin(event) == True:
            addHomework_flag = True
            add_homework()
    elif msg == 'Указать число':
        if userIsAdmin(event) == True:
            if addHomework_flag == True:
                setDate()
    elif msg == 'Указать день недели':
        if userIsAdmin(event) == True:
            if addHomework_flag == True:
                ShowWeekdays()
    elif msg == 'Отмена':
        if addHomework_flag == True:
            addHomework.clearStack()
            step_code = 0
            addHomework_flag = False
            mainMenu(event)
    elif msg == 'О боте':
        AboutText()
    else:
        if addHomework_flag == True:
            if step_code == 0:
                addHomework.setDate(msg)
                step_code = step_code + 1
                setLesson()
            elif step_code == 1:
                addHomework.setLesson(msg)
                step_code = step_code + 1
                setTask()
            elif step_code == 2:
                addHomework.setTask(msg)
                step_code = 0
                setHomework()
                addHomework_flag = False


if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = event.text
                commandDirect(event, msg)
