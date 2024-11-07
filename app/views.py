from django.http import HttpResponse
from django.shortcuts import render
import copy
from django.core.paginator import Paginator

questions = [
    {'id': 0, 
     'title': 'Какой язык программирования самый популярный?', 
     'text': 'Какая самая популярная в мире языков программирования на 2024 год?',
     'tags': ['Python', 'JavaScript', 'Programming'],
     'image': 'static/images/0.webp'}, 

    {'id': 1, 
     'title': 'Как стать веб-разработчиком?', 
     'text': 'Какие шаги нужно предпринять, чтобы стать веб-разработчиком?',
     'tags': ['Career', 'Web Development', 'Frontend', 'Backend'],
     'image': 'static/images/1.webp'},  

    {'id': 2, 
     'title': 'Что такое искусственный интеллект?', 
     'text': 'Что включает в себя термин искусственный интеллект и как он применяется?',
     'tags': ['AI', 'Machine Learning', 'Technology'],
     'image': 'static/images/2.webp'}, 

    {'id': 3, 
     'title': 'Как выбрать лучший хостинг для сайта?', 
     'text': 'Какие критерии важны при выборе хостинга для веб-сайта?',
     'tags': ['Hosting', 'Web Development', 'Tech'],
     'image': 'static/images/0.webp'}, 

    {'id': 4, 
     'title': 'Что такое блокчейн?', 
     'text': 'Объясните, что такое блокчейн и как он используется в криптовалютах.',
     'tags': ['Blockchain', 'Cryptocurrency', 'Technology'],
     'image': 'static/images/0.webp'},
     
    {'id': 5, 
     'title': 'Как работает квантовый компьютер?', 
     'text': 'Объясните, как работает квантовый компьютер и какие его преимущества.',
     'tags': ['Quantum Computing', 'Technology', 'Science'],
     'image': 'static/images/0.webp'},

    {'id': 6, 
     'title': 'Что такое Python и зачем он нужен?', 
     'text': 'Какие особенности языка Python делают его популярным среди разработчиков?',
     'tags': ['Python', 'Programming', 'Web Development'],
     'image': 'static/images/6.webp'},

    {'id': 7, 
     'title': 'Какие основы нужно знать для разработки на JavaScript?', 
     'text': 'Что нужно изучить новичку для того, чтобы начать разрабатывать на JavaScript?',
     'tags': ['JavaScript', 'Web Development', 'Frontend'],
     'image': 'static/images/7.png'},

    {'id': 8, 
     'title': 'Как повысить производительность работы с базами данных?', 
     'text': 'Какие методы оптимизации можно использовать для повышения производительности баз данных?',
     'tags': ['Databases', 'SQL', 'Performance'],
     'image': 'static/images/0.webp'},

    {'id': 9, 
     'title': 'Что такое микросервисы и как их использовать?', 
     'text': 'Какие преимущества дают микросервисы при разработке масштабируемых приложений?',
     'tags': ['Microservices', 'Software Architecture', 'Backend'],
     'image': 'static/images/0.webp'},
]

def index(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(questions, 3)
    page = paginator.page(page_num)
    context={
        'questions': page.object_list,
        'page_obj': page
        }
    return render(request, 'index.html', context)

def hot(request):
    hot_questions = copy.deepcopy(questions)
    hot_questions.reverse()
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(hot_questions, 3)
    page = paginator.page(page_num)

    context={
        'questions': page.object_list,
        'page_obj': page
        }
    return render(request, 'hot.html', context)

def question(request, question_id):
    question = questions[question_id]
    context = {'question': question}
    return render(request, 'question.html', context)