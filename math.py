import telebot
import random
import os
import time

# Укажите здесь свой токен, полученный от BotFather
bot = telebot.TeleBot(os.environ.get("Fun_arithmetic_key"))

@bot.message_handler(commands=['start'])
def start(message):
    welcome_message = "Привет! Давай сыграем в математическую викторину. Я задам тебе несколько вопросов, а ты должен дать правильные ответы.\n\nНачинаем игру!"
    bot.send_message(message.chat.id, welcome_message)
    start_quiz(message.chat.id)

def start_quiz(chat_id):
    ask_question(chat_id, 0, 0)

def ask_question(chat_id, question_number, correct_answers):
    arithmetic_sign = 2#random.randint(1, 4)
    if arithmetic_sign == 1:
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)
        num = num1 + num2
        question_text = f"Чему будет равняться {num1} + {num2} ="
    elif arithmetic_sign == 2:
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        if num2 > num1:
            num = num2 - num1
            question_text = f"Вычислите разницу: {num2} - {num1} ="
        else:
            num = num1 - num2
            question_text = f"Вычислите разницу: {num1} - {num2} ="
    elif arithmetic_sign == 3:
        num1 = random.randint(2, 10)
        num2 = random.randint(2, 10)
        num = num1 * num2
        question_text = f"Умножьте: {num1} * {num2} ="
    elif arithmetic_sign == 4:
        num2 = random.randint(2, 10)
        num1 = num2 * random.randint(1, 10)
        num = num1 // num2
        question_text = f"Поделите: {num1} / {num2} ="

    bot.send_message(chat_id, question_text)
    bot.register_next_step_handler_by_chat_id(chat_id, check_answer, num, question_number+1, correct_answers)

def check_answer(message, correct_answer, question_number, correct_answers):
    if message.text and message.text.isdigit() and int(message.text) == correct_answer:
        bot.send_message(message.chat.id, "Верно!")
        correct_answers += 1
    else:
        bot.send_message(message.chat.id, f"Неверно. Правильный ответ: {correct_answer}.")

    if question_number < 5:
        bot.send_message(message.chat.id, f"Вы ответили на {correct_answers} из {5} вопросов.")
        ask_question(message.chat.id, question_number, correct_answers)
    else:
        end_quiz(message.chat.id, correct_answers)

def end_quiz(chat_id, correct_answers):
    bot.send_message(chat_id, f"Игра окончена! Вы ответили верно на {correct_answers} из 5 вопросов.")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print("Опрос не удался из-за ошибки:", e)
        print("Попытка переподключения через 1 минуту.")
        time.sleep(60)