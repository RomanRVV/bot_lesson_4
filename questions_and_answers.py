import os
import re


def get_questions_and_answers(directory):

    folder_with_questions = os.listdir(directory)

    for question in folder_with_questions:
        with open(f"{directory}/{question}", "r", encoding="KOI8-R") as f:
            file_contents = f.read()

    file_sections = file_contents.split('\n\n')

    questions = []
    answers = []

    for file_section in file_sections:
        if "Вопрос " in file_section:
            questions.append(file_section)
        if "Ответ:" in file_section:
            answer = file_section.replace('Ответ:', '')
            answer_without_brackets = re.sub(r'\([^)]*\)', '', answer)
            correct_answer = answer_without_brackets.lstrip().strip('. ')

            answers.append(correct_answer)

    questions_and_answers = {}

    for question, answer in zip(questions, answers):
        questions_and_answers[question] = answer

    return questions_and_answers

