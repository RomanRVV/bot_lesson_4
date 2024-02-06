from environs import Env
import redis
import random

import logging

import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from enum import Enum

from questions_and_answers import get_questions_and_answers


logger = logging.getLogger(__name__)


class BotStates(Enum):
    QUESTION = 0
    SOLUTION_ATTEMPT = 1


def start(update: Update, context: CallbackContext) -> None:
    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                       ['Мой счет']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

    update.message.reply_text('Привет! Я бот для викторин',
                              reply_markup=reply_markup)

    return BotStates.QUESTION


def handle_new_question_request(update: Update, context: CallbackContext, r) -> None:
    user_id = update.effective_user.id

    questions_and_answers = get_questions_and_answers("questions")
    pair = list(questions_and_answers.items())
    random_pair = random.choice(pair)
    current_question = random_pair[0]

    r.set(user_id, current_question)
    update.message.reply_text(r.get(user_id))

    return BotStates.SOLUTION_ATTEMPT


def handle_solution_attempt(update, context, r):

    user_id = update.effective_user.id
    questions_and_answers = get_questions_and_answers("questions")
    correct_answer = questions_and_answers[r.get(user_id)]
    user_answer = update.message.text

    if correct_answer == user_answer:
        update.message.reply_text(f'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
        return BotStates.QUESTION
    else:
        update.message.reply_text(f'Неправильно… Попробуешь ещё раз?')
        return BotStates.SOLUTION_ATTEMPT


def handle_give_up(update, context, r):

    user_id = update.effective_user.id
    questions_and_answers = get_questions_and_answers("questions")
    correct_answer = questions_and_answers[r.get(user_id)]

    update.message.reply_text(f'Правильный ответ на последний вопрос - "{correct_answer}".'
                              f' Нажмите кнопку "Новый вопрос" для продолжения')

    return BotStates.QUESTION


def cancel(update, context):
    update.message.reply_text("Диалог отменен.")
    return ConversationHandler.END


def main() -> None:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logger.info("Запуск ТГ бота")

    env = Env()
    env.read_env()

    r = redis.Redis(host=env('REDIS_HOST'),
                    port=env('REDIS_PORT'),
                    password=env('REDIS_PASSWORD'),
                    decode_responses=True)

    updater = Updater(env('TG_API_TOKEN'))

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={

            BotStates.QUESTION: [MessageHandler(Filters.regex('Новый вопрос'),
                                                lambda update, context:
                                                handle_new_question_request(update, context, r))],
            BotStates.SOLUTION_ATTEMPT: [MessageHandler(Filters.regex('Сдаться'),
                                                        lambda update, context:
                                                        handle_give_up(update, context, r)),
                                         MessageHandler(Filters.text & ~Filters.command,
                                                        lambda update, context:
                                                        handle_solution_attempt(update, context, r))],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
