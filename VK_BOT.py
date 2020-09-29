import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
#
from bd_schedule_direct import scheduleDirect
import config
#
vk_session = vk_api.VkApi(token=config.token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
#
homework_flag = False
schedule_flag = False
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
    keyboard.add_button('В главное меню', color=VkKeyboardColor.SECONDARY)
    write_msg_withKeyboard(event.user_id, 'Выберите день недели', keyboard)


def ScheduleOrHomework():
    global homework_flag
    global schedule_flag
    #
    if schedule_flag == True:
        schedule(msg)
        schedule_flag = False
    elif homework_flag == True:
        homework(msg)
        homework_flag = False


def schedule(weekday):
    db = scheduleDirect('Data Base/db.db')
    lesson = db.get_Lesson(weekday)
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
    print('Кто-то зашел в раздел редактирования...')


def commandDirect(event, msg):
    global homework_flag
    global schedule_flag
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
        ScheduleOrHomework()
    elif msg == 'Вторник':
        ScheduleOrHomework()
    elif msg == 'Среда ':
        ScheduleOrHomework()
    elif msg == 'Четверг':
        ScheduleOrHomework()
    elif msg == 'Пятница':
        ScheduleOrHomework()
    elif msg == 'Суббота':
        ScheduleOrHomework()
    elif msg == 'Редактирование':
        if userIsAdmin(event) == True:
            editing()


if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = event.text
                commandDirect(event, msg)
