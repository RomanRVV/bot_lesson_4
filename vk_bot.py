import random

import redis
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from environs import Env

from questions_and_answers import get_questions_and_answers


def start_chatting(event, vk_api):
    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)

    keyboard.add_line()
    keyboard.add_button('Мой счет', color=VkKeyboardColor.PRIMARY)

    vk_api.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message='Привет! Я бот для викторин'
    )


def handle_new_question_request(event, vk_api, r):
    user_id = event.user_id

    questions_and_answers = get_questions_and_answers("questions")
    pair = list(questions_and_answers.items())
    random_pair = random.choice(pair)
    current_question = random_pair[0]
    r.set(user_id, current_question)

    vk_api.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message=r.get(user_id)
    )


def handle_solution_attempt(event, vk_api, r):
    user_id = event.user_id
    questions_and_answers = get_questions_and_answers("questions")
    correct_answer = questions_and_answers[r.get(user_id)]
    user_answer = event.text

    if correct_answer == user_answer:
        message = 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»'
    else:
        message = 'Неправильно… Попробуешь ещё раз?'

    vk_api.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message=message
    )


def handle_give_up(event, vk_api, r):
    user_id = event.user_id

    questions_and_answers = get_questions_and_answers("questions")
    correct_answer = questions_and_answers[r.get(user_id)]

    message = (f'Правильный ответ на последний вопрос - "{correct_answer}".'
               f' Нажмите кнопку "Новый вопрос" для продолжения')

    vk_api.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message=message
    )


def main():
    env = Env()
    env.read_env()

    r = redis.Redis(host="redis-19211.c322.us-east-1-2.ec2.cloud.redislabs.com",
                    port='19211',
                    password=env('REDIS_PASSWORD'),
                    decode_responses=True)

    vk_session = vk.VkApi(token=env('VK_API_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == 'Начать':
                start_chatting(event, vk_api)
            elif event.text == 'Новый вопрос':
                handle_new_question_request(event, vk_api, r)
            elif event.text == 'Сдаться':
                handle_give_up(event, vk_api, r)
            else:
                handle_solution_attempt(event, vk_api, r)


if __name__ == "__main__":
    main()
