from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import *

def index(request):
    questions = Question.objects.newest()
    page = pag(request, questions)

    context={'questions': page.object_list, 'page_obj': page}
    return render(request, 'index.html', context)


def hot(request):
    hot_questions = Question.objects.hot()
    page = pag(request, hot_questions)

    context={'questions': page.object_list, 'page_obj': page}
    return render(request, 'hot.html', context)


def question(request, question_id):
    question = Question.objects.get(id=question_id)
    answers = question.answer_set.all()

    page = pag(request, answers)
    context = {'question': question, 'is_question_page': True, 'answers': page.object_list, 'page_obj': page}
    return render(request, 'question.html', context)


def tag(request, tag_title):
    tag = Tag.objects.get(title=tag_title)
    questions_tag = tag.question_set.all()

    page = pag(request, questions_tag)
    context={'questions': page.object_list, 'page_obj': page, 'is_tag_page': True, 'tag_title': tag_title}
    return render(request, 'tagpage.html', context)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse(profile_edit))

    return render(request, 'login.html')


def logout(request):
    next_page = request.GET.get('next', reverse('login'))
    auth.logout(request)
    return redirect(next_page)

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse(index))
    else:
        form = UserForm()

    return render(request, 'signup.html', {"form": form})

def ask(request):
    user = request.user
    if request.method == "POST":
        form = QuestionAskForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()

            # Обработка тегов
            tags = form.cleaned_data.get('tags', '')
            tag_list = [tag.strip() for tag in tags.split(',')]
            for tag_name in tag_list:
                tag, _ = Tag.objects.get_or_create(title=tag_name)
                question.tags.add(tag)

            return redirect('question', question_id=question.id)
    return render(request, 'newquestion.html')

@login_required
def profile_edit(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile_edit'))
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'profile_edit.html', {"user": user, "form": form})



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
