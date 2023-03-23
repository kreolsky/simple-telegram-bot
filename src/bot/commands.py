import os
from telebot import TeleBot
from dotenv import load_dotenv
from .classes import MessageHandler

load_dotenv()
def parse_users(users_str):
    users_list = [x.strip() for x in os.getenv(users_str).split(',')]
    if not users_list[0]:
        return []
    return users_list

telebot_token = os.getenv("TELEGRAM_API_KEY")
allow_users = parse_users("ALLOW_USERS")
admin_users = parse_users("ADMIN_USERS")

bot = TeleBot(telebot_token)
app = MessageHandler()

@app.command('/whoiam')
def get_user_info(message):
    # Обработчик команды /whoiam
    # Отправляет пользователю его последнее сообщение как есть
    # Удаляет сообщений через 20 секунд
    # Доступна для всех пользователей
    user_id = str(message['message']['chat']['id'])
    message_id = bot.send_message(user_id, tools.dict_to_str(message)).message_id
    time.sleep(20)
    bot.delete_message(user_id, message_id)


@app.permission(allow_users)
@app.command('/start')
def start_command(message):
    # Обработчик команды /start
    # Доступна только для пользователей из списка ALLOW_USERS
    pass

@app.command()
@app.permission(allow_users)
def just_text():
    # Обработчик текста без какой либо команды
    # Доступна только для пользователей из списка ALLOW_USERS
    pass

def main(message):
    app.run(message)
