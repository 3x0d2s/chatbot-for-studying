import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import config

vk_session = vk_api.VkApi(token = config.token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def write_msg(user_id, message, keyboard):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id' : 0 , 'keyboard' : keyboard.get_keyboard() })

if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()

                if msg == 'привет':
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('Первая кнопка', color=VkKeyboardColor.SECONDARY)
                    write_msg(id, 'Привет', keyboard)

                if msg == 'первая кнопка':
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('Первая кнопка', color=VkKeyboardColor.SECONDARY)
                    write_msg(id, 'Ура', keyboard)