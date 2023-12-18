import random
import telebot
import os # Нужен для использования импорта токена из системы.
import time # Нужен для переподключения при разрыве соединения.

# Создание экземпляра бота с использованием токена из переменной окружения.
bot = telebot.TeleBot(os.environ.get("Random_number_key")) 

# Инициализация переменной количество попыток.
attempts = 10

# Обработчик команды "/start"
@bot.message_handler(commands=['start'])
def start_game(message):
    try:
        global secret_number
        secret_number = random.randint(1, 1000) # Генерация случайного числа от 1 до 1000.
        global attempts
        attempts = 10
        bot.send_message(
            chat_id=message.chat.id,
            text="Угадайте число от 1 до 1000:") # Отправка сообщения пользователю с просьбой угадать число.
        @bot.message_handler(content_types=['text']) # Обработчик сообщений с текстовым содержимым.
        def guess_number(message):
            global attempts
            try:
                num = int(message.text)
            except ValueError: # Обработка ошибки, если пользователь ввел не число.
                bot.send_message(
                    chat_id=message.chat.id,
                    text="Неверный ввод. Пробуйте снова. Пишите только цифры.")
                return
            effort = ''
            if attempts >=3 and attempts <=5:
                effort = 'попытки'
            elif attempts == 2:
                effort = 'попытка'
            else:
                effort = 'попыток'
            if num > 1000 or num < 1: # Обработка ошибки, если пользователь ввел число вне допустимого диапазона
                bot.send_message(
                    chat_id=message.chat.id,
                    text="Неверный ввод. Значения 1 до 1000.")

            elif num == secret_number and attempts == 10: # Обработка случая, когда пользователь угадал число с первой попытки
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f"Поздравляю! Вы угадали загаданное число с первой попытки, невероятный результат! Чтобы начать новую игру, напишите в чат /start")

            elif num == secret_number and attempts > 1: # Обработка случая, когда пользователь угадал число с нескольких попыток
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f"Отлично! Вы угадали загаданное число с {10 - attempts + 1} попытки. Чтобы начать новую игру, напишите в чат /start")

            elif num == secret_number and attempts == 1: # Обработка случая, когда пользователь угадал число с последней попытки
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f"Поздравляю! Вы угадали загаданное число с последней попытки, невероятное везение! Чтобы начать новую игру, напишите в чат /start")

            elif num < secret_number and attempts != 1: # Обработка случая, когда пользователь ввел число меньше
                attempts -= 1
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f"Ваше число: {num} меньше загаданного числа. Нужно большее число. У вас осталось {attempts} {effort}.")

            elif num > secret_number and attempts != 1: # Обработка случая, когда пользователь ввел число большее
                attempts -= 1
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f"Ваше число: {num} больше загаданного числа. Нужно меньшее число. У вас осталось {attempts} {effort}.")

            elif num != secret_number and attempts == 1: # Обработка случая, когда пользователь исчерпал все попытки
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f"Попытки кончились. Загаданное число {secret_number}. Повезет в другой раз. Чтобы начать новую игру, напишите в чат /start")
    except Exception as e: # Обработка всех исключений.
        print("An error occurred:", e.__class__.__name__)

# Бесконечный цикл для опроса новых сообщений от Telegram API.
# В случае обрыва интернета бот будет переподключаться к API пока не появится интернет.
while True: 
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        # Обработка исключений при ошибке опроса
        print("Опрос не удался из-за ошибки: ", e)
        print("Попытка переподключения через 1 минуту.")
        time.sleep(60)