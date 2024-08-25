import telebot
import psutil
import time
from telebot import types
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = telebot.TeleBot(os.getenv("TOKEN"))


def check_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > 50:
        return cpu_usage
    return None


def get_top_processes():
    processes = []

    for proc in psutil.process_iter(["pid", "name", "cpu_percent"]):
        processes.append(proc.info)

    top_processes = sorted(
        processes, key=lambda proc: proc["cpu_percent"], reverse=True
    )
    return top_processes


def send_cpu_alert(id):
    cpu_usage = check_cpu_usage()
    print(cpu_usage)
    if cpu_usage:
        top_processes = get_top_processes()
        message = f"Внимание! Загрузка CPU: {cpu_usage}%\n\nТоп 3 процесса по потреблению CPU:\n"

        for proc in top_processes[:3]:
            message += f"PID: {proc['pid']}, Имя: {proc['name']}, CPU: {proc['cpu_percent']}%\n"
        bot.send_message(id, message)


@bot.message_handler(commands=["start"])
def start_monitoring(message):

    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton(text="Начать мониторинг")
    markup.add(btn1)

    bot.send_message(
        message.from_user.id, text="Бот запущен. Мониторинг начат.", reply_markup=markup
    )
    while True:
        send_cpu_alert(message.from_user.id)
        time.sleep(60)  # Проверка каждые 60 секунд


bot.polling()
