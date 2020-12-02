#
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from bd_direct import bdDirect
from directHomework import Homework
from check_InputData import *
import config
import datetime
#
vk_session = vk_api.VkApi(token=config.token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
Homework = Homework()
users = None
#


def write_msg(user_id, message):
    vk_session.method('messages.send', {
                      'user_id': user_id, 'message': str(message), 'random_id': 0})


def write_msg_withKeyboard(user_id, message, keyboard):
    vk_session.method('messages.send', {'user_id': user_id, 'message': str(
        message), 'random_id': 0, 'keyboard': keyboard.get_keyboard()})


def mainMenuKeyboard(event):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Расписание', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Домашнее задание', color=VkKeyboardColor.POSITIVE)
    if userIsAdmin(event) == True:
        keyboard.add_line()
        keyboard.add_button(
            'Редактирование', color=VkKeyboardColor.SECONDARY)
    return keyboard


def editingKeyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Добавить домашнее задание',
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
    db = bdDirect('Data Base/db.db')
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
            db = bdDirect('Data Base/db.db')
            db.add_user(event.user_id)
            db.close()
            getUsers()
    else:
        db = bdDirect('Data Base/db.db')
        db.add_user(event.user_id)
        db.close()
        getUsers()


def userIsAdmin(event):
    user_id = event.user_id
    for user in range(len(users)):
        if user_id == users[user][0]:
            return users[user][1]  # True or False


def ShowWeekdays(event):
    db = bdDirect('Data Base/db.db')
    Homework_flag = db.getUserHomewFlag(event.user_id)
    Schedule_flag = db.getUserSchedFlag(event.user_id)
    addHomework_flag = db.getUserAddHomewFlag(event.user_id)
    db.close()
    #
    if addHomework_flag == True:
        msg = 'После выбора домашнее задание автоматически запишется на ближайший выбранный день недели.'
    else:
        msg = 'Выберите день недели или укажите дату...'
    keyboard = VkKeyboard(one_time=False)
    if Schedule_flag == True or Homework_flag == True:
        if Homework_flag == True:
            keyboard.add_button(
                'Указать число', color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
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
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def ScheduleOrOperHomework(event, msg):
    db = bdDirect('Data Base/db.db')
    addHomework_flag = db.getUserAddHomewFlag(event.user_id)
    Homework_flag = db.getUserHomewFlag(event.user_id)
    Schedule_flag = db.getUserSchedFlag(event.user_id)
    delHomework_flag = db.getUserDelHomewFlag(event.user_id)
    step_code = db.getUserStepCode(event.user_id)
    #
    if Schedule_flag == True:
        schedule(msg)
        db.changeUserSchedFlag(event.user_id, False)
    elif Homework_flag == True:
        homework(event, msg)
        db.changeUserHomewFlag(event.user_id, False)
    elif addHomework_flag == True or delHomework_flag == True:
        Homework.setWeekday(msg)
        db.changeUserStepCode(event.user_id, (step_code + 1))
        setLesson()
    db.close()


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
    if weekday != 'Воскресенье':
        db = bdDirect('Data Base/db.db')
        lesson = db.get_Lesson(weekday)
        db.close()
        #
        listLessons = []
        rowcount = len(lesson)
        for row in range(rowcount):
            start_time = lesson[row][2]
            end_time = lesson[row][3]
            lesson_name = lesson[row][4]
            cabinet = lesson[row][5]
            msg = str('🔹 ' + start_time + '-' + end_time +
                      ' ' + lesson_name + ' | ' + str(cabinet))
            listLessons.append(msg)
        msg = '📝 Расписание уроков на ' + Accusative(weekday) + ':'
        for row in listLessons:
            msg = msg + '\n' + row
    elif weekday == 'Воскресенье':
        msg = 'Уроки в воскресенье? Всё нормально? Лучше поспи, отдохни, хорошо покушай.'
    write_msg_withKeyboard(event.user_id, msg, mainMenuKeyboard(event))


def homework(event, weekday=None, mode=0):
    if weekday != None:
        Homework.getDateByWeekday(weekday)
    else:
        Homework.setWeekday()
        weekday = Homework.getWeekday()
    date = Homework.getDate()
    if weekday != 'Воскресенье':
        db = bdDirect('Data Base/db.db')
        homework_tasks = db.get_Homework(date)
        db.close()
        rowcount = len(homework_tasks)
        if rowcount > 0:
            listHomework = []
            for row in range(rowcount):
                lesson_name = homework_tasks[row][0]
                task = homework_tasks[row][1]
                msg = str('♦ ' + lesson_name + ' - ' + task)
                listHomework.append(msg)
            msg = 'Домашнее задание на ' + \
                Accusative(weekday) + ' (' + date + ')' + ':'
            for rows in listHomework:
                msg = msg + '\n' + rows
        else:
            if mode == 0:
                if weekday == 'Понедельник' or weekday == 'Вторник' or weekday == 'Четверг':
                    msg = 'На ближайший ' + weekday.lower() + ' нет домашнего задания.'
                else:
                    msg = 'На ближайшую ' + \
                        Accusative(weekday).lower() + ' нет домашнего задания.'
            elif mode == 1:
                msg = 'На сегодня нет домашнего задания.'
            elif mode == 2:
                msg = 'На завтра нет домашнего задания.'
            elif mode == 3:
                if weekday == 'Понедельник' or weekday == 'Вторник' or weekday == 'Четверг':
                    msg = 'На ' + \
                        Accusative(weekday).lower() + ' ' + \
                        date + ' нет домашнего задания.'
                else:
                    msg = 'На ' + \
                        Accusative(weekday).lower() + ' ' + \
                        date + ' нет домашнего задания.'
    elif weekday == 'Воскресенье':
        msg = 'Домашнее задание на воскресенье? Совсем переучились? Отдыхайте, неблагополучные!'
    Homework.clearStack()
    db = bdDirect('Data Base/db.db')
    db.changeUserHomewFlag(event.user_id, False)
    db.close()
    write_msg_withKeyboard(event.user_id, msg, mainMenuKeyboard(event))


def OperTodayTomorrow(event):
    db = bdDirect('Data Base/db.db')
    Schedule_flag = db.getUserSchedFlag(event.user_id)
    Homework_flag = db.getUserHomewFlag(event.user_id)
    #
    if Schedule_flag == True or Homework_flag == True:
        idWeekday = datetime.datetime.now().weekday()
        weekdays = ['Понедельник', 'Вторник', 'Среда',
                    'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        if Schedule_flag == True:
            db.changeUserSchedFlag(event.user_id, False)
            if msg == 'На сегодня':
                schedule(weekdays[idWeekday])
            elif msg == 'На завтра':
                if idWeekday == 6:
                    '''  Самый большой костыль этого кода здесь :) '''
                    idWeekday = -1
                schedule(weekdays[idWeekday + 1])
        elif Homework_flag == True:
            db.changeUserHomewFlag(event.user_id, False)
            if msg == 'На сегодня':
                homework(event, weekdays[idWeekday], 1)
            elif msg == 'На завтра':
                if idWeekday == 6:
                    '''  Обманул, еще здесь костыль :) '''
                    idWeekday = -1
                homework(event, weekdays[idWeekday + 1], 2)
    db.close()


def getDateByLesson(lesson):
    db = bdDirect('Data Base/db.db')
    lessons = db.get_allLesson()
    db.close()
    #
    lesson = msg
    main_list = []
    #
    for step in range(len(lessons)):
        if lesson == lessons[step][1]:  # 0 - weekday 1 - lesson
            weekday = lessons[step][0]
            date = datetime.datetime.strptime(
                Homework.getDateByWeekday(weekday, 1), '%d.%m.%Y')
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
                    return lesson + ' будет во ' + Accusative(step[1]) + ' (' + str(step[0].strftime('%d.%m.%Y')) + ')'
                else:
                    return lesson + ' будет в ' + Accusative(step[1]) + ' (' + str(step[0].strftime('%d.%m.%Y')) + ')'
        if main_list[0][1] == 'Вторник':
            return lesson + ' будет во ' + Accusative(main_list[0][1]) + ' (' + str(main_list[0][0].strftime('%d.%m.%Y')) + ')'
        else:
            return lesson + ' будет в ' + Accusative(main_list[0][1]) + ' (' + str(main_list[0][0].strftime('%d.%m.%Y')) + ')'
    else:
        return 'Такой урок не был найден.'


def OperWithDelOrAddHomework(event, msg):
    db = bdDirect('Data Base/db.db')
    Homework_flag = db.getUserHomewFlag(event.user_id)
    addHomework_flag = db.getUserAddHomewFlag(event.user_id)
    delHomework_flag = db.getUserDelHomewFlag(event.user_id)
    getLessonDate_flag = db.getUserGetLessDateFlag(event.user_id)
    step_code = db.getUserStepCode(event.user_id)
    #
    if addHomework_flag == True or delHomework_flag == True or Homework_flag == True or getLessonDate_flag == True:
        # Date
        if step_code == 0:
            if check_Date(msg) == True:
                Homework.setDate(msg)
                if Homework_flag == True:
                    homework(event, None, 3)
                else:
                    db.changeUserStepCode(event.user_id, (step_code + 1))
                    setLesson()
            else:
                msg = 'Ошибка даты: неверный формат.'
                write_msg(event.user_id, msg)
                setDate()
        if userIsAdmin(event) == True:
            # Lesson
            if step_code == 1:
                if check_Lesson(msg) == True:
                    if addHomework_flag == True:
                        Homework.setLesson(msg)
                        db.changeUserStepCode(event.user_id, (step_code + 1))
                        setTask()
                    elif delHomework_flag == True:
                        Homework.setLesson(msg)
                        db.changeUserStepCode(event.user_id, 0)
                        db.changeUserDelHomewFlag(event.user_id, False)
                        delHomework()
                        Homework.clearStack()
                    elif getLessonDate_flag == True:
                        msg = getDateByLesson(msg)
                        db.changeUserStepCode(event.user_id, 0)
                        db.changeUserGetLessDateFlag(event.user_id, False)
                        write_msg_withKeyboard(
                            event.user_id, msg, editingKeyboard())
                else:
                    msg = 'Ошибка названия урока: длина не может превышать 16 символов.'
                    write_msg(event.user_id, msg)
                    setLesson()
            # Task
            elif step_code == 2:
                if check_Tasks(msg) == True:
                    Homework.setTask(msg)
                    db.changeUserStepCode(event.user_id, 0)
                    db.changeUserAddHomewFlag(event.user_id, False)
                    setHomework()
                    Homework.clearStack()
                else:
                    msg = 'Ошибка задач: длина не может превышать 512 символов.'
                    write_msg(event.user_id, msg)
                    setTask()
    else:
        msg = 'Данной команды не существует.'
        write_msg(event.user_id, msg)
    db.close()


def editing():
    msg = 'Выберите действие...'
    write_msg_withKeyboard(event.user_id, msg, editingKeyboard())


def add_homework():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Указать число',
                        color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Указать день недели',
                        color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Отмена', color=VkKeyboardColor.POSITIVE)
    msg = 'Выберите вариант указания даты сдачи домашнего задания...'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def del_homework():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Указать число',
                        color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Удалить старое ДЗ', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Отмена', color=VkKeyboardColor.POSITIVE)
    msg = 'Выберите действие...'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def clearOldHomework():
    db = bdDirect('Data Base/db.db')
    allHomework = db.get_allHomework()
    wasItDeleted = False
    #
    rowcount = len(allHomework)
    if rowcount > 0:
        now = datetime.datetime.now().replace(
            hour=0, second=0, microsecond=0, minute=0)
        for row in range(rowcount):
            date = allHomework[row][0]
            homew_date = datetime.datetime.strptime(
                date, '%d.%m.%Y')
            if now > homew_date:
                lesson = allHomework[row][1]
                db.del_Homework(date, lesson)
                if wasItDeleted == False:
                    wasItDeleted = True
    db.close()
    if wasItDeleted == True:
        msg = 'Всё старое домашнее задание было удалено.'
    else:
        msg = 'Старое домашнее задание не было найдено.'
    write_msg_withKeyboard(event.user_id, msg, mainMenuKeyboard(event))


def setDate():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    msg = 'Введите число в формате (День).(Месяц).(Год). Например 03.11.2018'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def setLesson():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    msg = 'Введите название урока...'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def setTask():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    msg = 'Введите все задачи...'
    write_msg_withKeyboard(event.user_id, msg, keyboard)


def setHomework():
    date = Homework.getDate()
    weekDay = Homework.getWeekday()
    lesson = Homework.getLesson()
    task = Homework.getTask()
    #
    db = bdDirect('Data Base/db.db')
    if db.check_Homework(date, lesson) == False:
        db.add_Homework(date, weekDay, lesson, task)
        if db.check_Homework(date, lesson) == True:
            msg = 'Домашнее задание добавлено!'
            write_msg_withKeyboard(event.user_id, msg, mainMenuKeyboard(event))
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


def delHomework():
    date = Homework.getDate()
    lesson = Homework.getLesson()
    #
    db = bdDirect('Data Base/db.db')
    if db.check_Homework(date, lesson) == True:
        db.del_Homework(date, lesson)
        db.close()
        msg = 'Домашнее задание удалено!'
        write_msg_withKeyboard(event.user_id, msg, mainMenuKeyboard(event))
    else:
        msg = 'Такого домашнего задания не существует.'
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Удаление домашнего задания',
                            color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
        write_msg_withKeyboard(event.user_id, msg, keyboard)


def commandDirect(event, msg):
    db = bdDirect('Data Base/db.db')
    Homework_flag = db.getUserHomewFlag(event.user_id)
    Schedule_flag = db.getUserSchedFlag(event.user_id)
    addHomework_flag = db.getUserAddHomewFlag(event.user_id)
    delHomework_flag = db.getUserDelHomewFlag(event.user_id)
    #
    if msg == 'Start' or msg == 'Начать':
        write_msg_withKeyboard(
            event.user_id, 'Главное меню', mainMenuKeyboard(event))
    elif msg == 'В главное меню':
        if Schedule_flag == True:
            db.changeUserSchedFlag(event.user_id, False)
        elif Homework_flag == True:
            db.changeUserHomewFlag(event.user_id, False)
        elif addHomework_flag == True:
            Homework.clearStack()
            db.changeUserAddHomewFlag(event.user_id, False)
        elif delHomework_flag == True:
            Homework.clearStack()
            db.changeUserDelHomewFlag(event.user_id, False)
        write_msg_withKeyboard(
            event.user_id, 'Главное меню', mainMenuKeyboard(event))
    elif msg == 'Расписание':
        db.changeUserSchedFlag(event.user_id, True)
        ShowWeekdays(event)
    elif msg == 'Домашнее задание':
        db.changeUserHomewFlag(event.user_id, True)
        ShowWeekdays(event)
    elif msg == 'На сегодня' or msg == 'На завтра':
        OperTodayTomorrow(event)
    elif (msg == 'Понедельник' or msg == 'Вторник' or msg == 'Среда'
          or msg == 'Четверг' or msg == 'Пятница' or msg == 'Суббота'):
        ScheduleOrOperHomework(event, msg)
    elif msg == 'Редактирование':
        if userIsAdmin(event) == True:
            editing()
    elif msg == 'Добавить домашнее задание':
        if userIsAdmin(event) == True:
            db.changeUserAddHomewFlag(event.user_id, True)
            add_homework()
    elif msg == 'Удаление домашнего задания':
        if userIsAdmin(event) == True:
            db.changeUserDelHomewFlag(event.user_id, True)
            del_homework()
    elif msg == 'Указать число':
        if Homework_flag or addHomework_flag == True or delHomework_flag == True:
            setDate()
    elif msg == 'Удалить старое ДЗ':
        if userIsAdmin(event) == True:
            if delHomework_flag == True:
                clearOldHomework()
    elif msg == 'Указать день недели':
        if userIsAdmin(event) == True:
            if addHomework_flag == True:
                ShowWeekdays(event)
    elif msg == 'Когда следующий урок?':
        if userIsAdmin(event) == True:
            db.changeUserGetLessDateFlag(event.user_id, True)
            db.changeUserStepCode(event.user_id, 1)
            setLesson()
    elif msg == 'Отмена':
        if addHomework_flag == True:
            Homework.clearStack()
            db.changeUserAddHomewFlag(event.user_id, False)
            db.changeUserStepCode(event.user_id, 0)
        elif delHomework_flag == True:
            Homework.clearStack()
            db.changeUserDelHomewFlag(event.user_id, False)
            db.changeUserStepCode(event.user_id, 0)
        elif Homework_flag == True:
            Homework.clearStack()
            db.changeUserHomewFlag(event.user_id, False)
            db.changeUserStepCode(event.user_id, 0)
        write_msg_withKeyboard(
            event.user_id, 'Главное меню', mainMenuKeyboard(event))
    else:
        OperWithDelOrAddHomework(event, msg)
    db.close()


if __name__ == '__main__':
    getUsers()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                checkUser(event)
                msg = event.text
                commandDirect(event, msg)
