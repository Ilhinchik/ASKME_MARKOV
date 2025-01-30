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

def get_base_context():
    print(Profile.objects.get_top_users())
    return {
        'tags': Tag.objects.popular(),
        'top_users_profiles': Profile.objects.get_top_users(),
    }

def index(request):
    questions = Question.objects.newest()
    page = pag(request, questions)

    context={'questions': page.object_list, 'page_obj': page}
    context.update(get_base_context())
    return render(request, 'index.html', context)


def hot(request):
    hot_questions = Question.objects.hot()
    page = pag(request, hot_questions)

    context={'questions': page.object_list, 'page_obj': page}
    context.update(get_base_context())
    return render(request, 'hot.html', context)


def question(request, question_id):
    user = request.user
    question = Question.objects.get(id=question_id)
    answers = question.answers.order_by('-created_at', '-id')
    if request.method == 'POST':
        print("POST данные:", request.POST)
        if not request.user.is_authenticated:
            return redirect('login')
        answer_form = AnswerForm(request.POST, question_id=question_id, user=request.user)
        if answer_form.is_valid():
            answer = answer_form.save()
            return redirect(reverse('question', args=[question_id]) + f'#answer-{answer.pk}')

    page = pag(request, answers)
    context = {'question': question, 'is_question_page': True, 'answers': page.object_list, 'page_obj': page}
    context.update(get_base_context())
    return render(request, 'question.html', context)


def tag(request, tag_title):
    tag = Tag.objects.get(title=tag_title)
    questions = Question.objects.tagged(tag.title)

    page = pag(request, questions)
    context={'questions': page.object_list, 'page_obj': page, 'is_tag_page': True, 'tag_title': tag_title}
    context.update(get_base_context())
    return render(request, 'tagpage.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next') or request.GET.get('continue', 'index'))

    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(request.GET.get('next') or request.GET.get('continue', 'index'))
            login_form.add_error(None, 'Incorrect username or password')
    context = get_base_context()
    context['form'] = login_form
    return render(request, 'login.html', context)


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
    context = {}
    context.update(get_base_context())
    return render(request, 'newquestion.html', context)

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
    context = {"user": user, "form": form}
    context.update(get_base_context())
    return render(request, 'profile_edit.html', context)



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
