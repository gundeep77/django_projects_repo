import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_quiz.settings')
django.setup()
from epicQuiz.models import ComputerQuiz
from epicQuiz.models import ScienceQuiz
from epicQuiz.models import GKQuiz
import json

computer_file = open('epicQuiz/static/computer.json')
science_file = open('epicQuiz/static/science.json')
gk_file = open('epicQuiz/static/gk.json')

computer_data = json.load(computer_file)
science_data = json.load(science_file)
gk_data = json.load(gk_file)


for ele in computer_data['results']:
    my_ques = ComputerQuiz(question = ele['question'], option1 = ele['correct_answer'], option2 = ele['incorrect_answers'][0], option3 = ele['incorrect_answers'][1], option4 = ele['incorrect_answers'][2], correct_ans = ele['correct_answer'])
    my_ques.save()


for ele in science_data['results']:
    my_ques = ScienceQuiz(question = ele['question'], option1 = ele['correct_answer'], option2 = ele['incorrect_answers'][0], option3 = ele['incorrect_answers'][1], option4 = ele['incorrect_answers'][2], correct_ans = ele['correct_answer'])
    my_ques.save()


for ele in gk_data['results']:
    my_ques = GKQuiz(question = ele['question'], option1 = ele['correct_answer'], option2 = ele['incorrect_answers'][0], option3 = ele['incorrect_answers'][1], option4 = ele['incorrect_answers'][2], correct_ans = ele['correct_answer'])
    my_ques.save()

