import os
from flask import Flask
from flask import request
from flask import abort

from rq import Queue
from redis import Redis
from dotenv import load_dotenv
import rq_dashboard

from bot.commands import main as parser

load_dotenv()
redis_host = os.getenv("REDIS_HOST")
telebot_token = os.getenv("TELEGRAM_API_KEY")

redis_conn = Redis.from_url(redis_host)
queue = Queue('bot', connection=redis_conn)

def bot_request(request, queue, parser):
    # Содержимое сообщения из реквеста
    message = request.get_json()
    # Складываем обработку запроса и его выполнение в очередь
    queue.enqueue(parser, message)

if __name__ == "__main__":
    
