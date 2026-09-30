import os
import re
import time

import requests

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)


# Разрешаем запросы только от нашего локального frontend.
# После публикации сюда добавим настоящий адрес сайта.

FRONTEND_ORIGIN = os.getenv(
    "FRONTEND_ORIGIN",
    "https://roman-webdev.github.io"
)

ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    FRONTEND_ORIGIN
]

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": ALLOWED_ORIGINS
        }
    }
)


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


# -----------------------------------
# НАСТРОЙКИ
# -----------------------------------

MAX_NAME_LENGTH = 50
MAX_PHONE_LENGTH = 25
MAX_CAR_LENGTH = 100
MAX_SERVICE_LENGTH = 50

RATE_LIMIT_SECONDS = 10


# Здесь временно храним время последней заявки от каждого IP.
# Для учебного проекта этого достаточно.
# Позже разберём нормальный rate limiting.

last_requests = {}


# -----------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# -----------------------------------

def clean_text(value):
    return str(value or "").strip()


def is_valid_phone(phone):

    cleaned_phone = re.sub(
        r"[\s()-]",
        "",
        phone
    )

    pattern = r"^\+?\d{10,15}$"

    return bool(
        re.fullmatch(
            pattern,
            cleaned_phone
        )
    )


def check_rate_limit(ip_address):

    current_time = time.time()

    last_request_time = last_requests.get(ip_address)

    if last_request_time is not None:

        seconds_passed = (
            current_time - last_request_time
        )

        if seconds_passed < RATE_LIMIT_SECONDS:
            return False

    last_requests[ip_address] = current_time

    return True


# -----------------------------------
# API
# -----------------------------------

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "DRIVEFIX API"
    }), 200

@app.route("/api/booking", methods=["POST"])
def create_booking():

    # -------------------------------
    # RATE LIMIT
    # -------------------------------

    client_ip = request.remote_addr or "unknown"

    if not check_rate_limit(client_ip):

        return jsonify({
            "success": False,
            "message": (
                "Слишком много запросов. "
                "Попробуйте немного позже."
            )
        }), 429


    # -------------------------------
    # JSON
    # -------------------------------

    if not request.is_json:

        return jsonify({
            "success": False,
            "message": "Ожидаются данные в формате JSON."
        }), 415


    data = request.get_json(
        silent=True
    )


    if not isinstance(data, dict):

        return jsonify({
            "success": False,
            "message": "Некорректные данные заявки."
        }), 400


    # -------------------------------
    # ПОЛУЧАЕМ ДАННЫЕ
    # -------------------------------

    name = clean_text(
        data.get("name")
    )

    phone = clean_text(
        data.get("phone")
    )

    car = clean_text(
        data.get("car")
    )

    service = clean_text(
        data.get("service")
    )


    # -------------------------------
    # ПРОВЕРКА ИМЕНИ
    # -------------------------------

    if len(name) < 2:

        return jsonify({
            "success": False,
            "message": "Введите корректное имя."
        }), 400


    if len(name) > MAX_NAME_LENGTH:

        return jsonify({
            "success": False,
            "message": "Имя слишком длинное."
        }), 400


    # -------------------------------
    # ПРОВЕРКА ТЕЛЕФОНА
    # -------------------------------

    if len(phone) > MAX_PHONE_LENGTH:

        return jsonify({
            "success": False,
            "message": "Номер телефона слишком длинный."
        }), 400


    if not is_valid_phone(phone):

        return jsonify({
            "success": False,
            "message": "Введите корректный номер телефона."
        }), 400


    # -------------------------------
    # ПРОВЕРКА АВТОМОБИЛЯ
    # -------------------------------

    if len(car) > MAX_CAR_LENGTH:

        return jsonify({
            "success": False,
            "message": "Название автомобиля слишком длинное."
        }), 400


    # -------------------------------
    # ПРОВЕРКА УСЛУГИ
    # -------------------------------

    if not service:

        return jsonify({
            "success": False,
            "message": "Выберите услугу."
        }), 400


    if len(service) > MAX_SERVICE_LENGTH:

        return jsonify({
            "success": False,
            "message": "Название услуги слишком длинное."
        }), 400


    # -------------------------------
    # TELEGRAM
    # -------------------------------

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:

        print(
            "Ошибка: Telegram не настроен."
        )

        return jsonify({
            "success": False,
            "message": "Ошибка настройки сервера."
        }), 500


    message = (
        "🔧 Новая заявка DRIVEFIX\n\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"🚗 Автомобиль: {car or 'Не указан'}\n"
        f"🛠 Услуга: {service}"
    )


    telegram_url = (
        "https://api.telegram.org/"
        f"bot{TELEGRAM_BOT_TOKEN}/"
        "sendMessage"
    )


    try:

        telegram_response = requests.post(
            telegram_url,
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message
            },
            timeout=10
        )


        if not telegram_response.ok:

            print(
                "Telegram error:",
                telegram_response.text
            )

            return jsonify({
                "success": False,
                "message": (
                    "Не удалось отправить заявку."
                )
            }), 502


    except requests.RequestException as error:

        print(
            "Ошибка соединения с Telegram:",
            error
        )

        return jsonify({
            "success": False,
            "message": (
                "Ошибка соединения с Telegram."
            )
        }), 502


    # -------------------------------
    # УСПЕХ
    # -------------------------------

    return jsonify({
        "success": True,
        "message": "Заявка успешно отправлена."
    }), 200


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )