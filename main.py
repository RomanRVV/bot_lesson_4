import os
from pprint import pprint

directory = "questions"

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
        answers.append(file_section)

questions_and_answers = {}

for question, answer in zip(questions, answers):
    questions_and_answers[question] = answer


