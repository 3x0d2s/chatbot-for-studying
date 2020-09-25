import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
#
from bd_schedule_direct import scheduleDirect
import config
#
vk_session = vk_api.VkApi(token = config.token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
#
isStarted = False
#
def write_msg(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': str(message), 'random_id' : 0})

def write_msg_withKeyboard(user_id, message, keyboard):
    vk_session.method('messages.send', {'user_id': user_id, 'message': str(message), 'random_id' : 0 , 'keyboard' : keyboard.get_keyboard() })

def mainMenu (): 
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Расписание', color=VkKeyboardColor.SECONDARY)
    write_msg_withKeyboard(event.user_id, 'Hi!', keyboard)

def schedule ():
    db = scheduleDirect('Data Base/db.db')
    lesson = db.get_Lesson(1)
    #
    listLessons = []
    rowcount = len(lesson)
    row = 0
    while row < rowcount:
        start_time = lesson[row][1]
        end_time = lesson[row][2]
        lesson_name = lesson[row][3]
        cabinet = lesson[row][4]
        msg = str(str(row + 1) + ') ' + lesson_name + ' ' + start_time + '-' + end_time + ' | ' + str(cabinet))
        #
        listLessons.append(msg)
        row = row + 1
    msg = 'Расписание уроков:'
    for row in listLessons:
        msg =  msg + '\n' + row
    write_msg(event.user_id, msg)

def commandDirect(msg): 
    if msg == 'Start':
        mainMenu()
    if msg == 'Расписание':
        schedule()

if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = event.text
                commandDirect(msg)
                
