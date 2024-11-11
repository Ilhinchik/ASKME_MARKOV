from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *

def index(request):
    questions = Question.objects.newest()
    page = pag(request, questions)

    context={'questions': page.object_list, 'page_obj': page}
    return render(request, 'index.html', context)


def hot(request):
    hot_questions = questions = Question.objects.hot()
    page = pag(request, hot_questions)

    context={'questions': page.object_list, 'page_obj': page}
    return render(request, 'hot.html', context)


def question(request, question_id):
    question = Question.objects.get(id=question_id)
    context = {'question': question, 'is_question_page': True}
    return render(request, 'question.html', context)


def tag(request, tag_title):
    tag = Tag.objects.get(title=tag_title)
    questions_tag = tag.question_set.all()

    page = pag(request, questions_tag)
    context={'questions': page.object_list, 'page_obj': page, 'is_tag_page': True, 'tag_title': tag_title}
    return render(request, 'tagpage.html', context)


def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'newquestion.html')

def setting(request):
    return render(request, 'setting.html')



def pag(request, q):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(q, 3)

    try:
        page = paginator.page(page_num)

    except PageNotAnInteger:
        page = paginator.page(1)

    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page
