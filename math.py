import telebot
import random
import os
import time

# Укажите здесь свой токен, полученный от BotFather
bot = telebot.TeleBot(os.environ.get("Fun_arithmetic_key"))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Давай сыграем в математическую викторину. Я задам тебе несколько вопросов, а ты должен дать правильные ответы.")
    ask_question(message.chat.id)

def ask_question(chat_id):
    sing = random.randint(1, 4)
    if sing == 1:
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)
        num = num1 + num2
        question_text = f"Чему будет равняться {num1} + {num2} ="
    elif sing == 2:
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        num = num1 - num2
        question_text = f"Вычислите разницу: {num1} - {num2} ="
    elif sing == 3:
        num1 = random.randint(2, 10)
        num2 = random.randint(2, 10)
        num = num1 * num2
        question_text = f"Умножьте: {num1} * {num2} ="
    elif sing == 4:
        num2 = random.randint(2, 10)
        num1 = num2 * random.randint(1, 10)
        num = num1 // num2
        question_text = f"Поделите: {num1} / {num2} ="

    bot.send_message(chat_id, question_text)
    bot.register_next_step_handler_by_chat_id(chat_id, check_answer, num)

def check_answer(message, correct_answer):
    if message.text and message.text.isdigit() and int(message.text) == correct_answer:
        bot.send_message(message.chat.id, "Верно!")
    else:
        bot.send_message(message.chat.id, f"Неверно. Правильный ответ: {correct_answer}.")

    ask_question(message.chat.id)


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print("Опрос не удался из-за ошибки:", e)
        print("Попытка переподключения через 1 минуту.")
        time.sleep(60)