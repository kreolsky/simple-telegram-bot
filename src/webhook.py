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

app = Flask(__name__)
rq_dashboard.default_settings.RQ_DASHBOARD_REDIS_HOST = redis_host
app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/bot/simple-telegram-bot/rqX")

redis_conn = Redis.from_url(redis_host)
queue = Queue('bot', connection=redis_conn)

def bot_request(request, queue, parser):
    if request.method == 'POST':
        # Содержимое сообщения из реквеста
        message = request.get_json()
        # Складываем обработку запроса и его выполнение в очередь
        queue.enqueue(parser, message)
        return 'OK'

    return abort(404)

@app.route('/bot/' + telebot_token, methods=['POST', 'GET'])
def translator_bot():
    return bot_request(request, queue, parser)

if __name__ == "__main__":
    app.run()
