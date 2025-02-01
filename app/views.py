from django.db.models import Exists, OuterRef
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST

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

    if request.user.is_authenticated:
        questions = questions.annotate(
            is_liked=Exists(
                QuestionLike.objects.filter(user=request.user, question=OuterRef('pk'))
            )
        )
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
    is_liked = False
    question = Question.objects.get(id=question_id)
    answers = question.answers.order_by('-created_at', '-id')
    if request.user.is_authenticated:
        is_liked = QuestionLike.objects.filter(user=request.user, question=question).exists()
        answers = answers.annotate(
            is_liked=Exists(
                AnswerLike.objects.filter(user=request.user, answer=OuterRef('pk'))
            )
        )

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
    context['is_liked'] = is_liked
    context.update(get_base_context())
    return render(request, 'question.html', context)


def tag(request, tag_title):
    tag = Tag.objects.get(title=tag_title)
    questions = Question.objects.tagged(tag.title)

    if request.user.is_authenticated:
        questions = questions.annotate(
            is_liked=Exists(
                QuestionLike.objects.filter(user=request.user, question=OuterRef('pk'))
            )
        )

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

@require_POST
def question_like(request, question_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    question = get_object_or_404(Question, pk=question_id)
    like, like_created = QuestionLike.objects.get_or_create(user=request.user, question=question)

    liked = True
    if not like_created:
        like.delete()
        liked = False

    question.save()
    return JsonResponse(
        {'question_likes_count': QuestionLike.objects.filter(question=question).count(), 'liked': liked})

@require_POST
def answer_like(request, answer_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    answer = get_object_or_404(Answer, pk=answer_id)
    like, like_created = AnswerLike.objects.get_or_create(user=request.user, answer=answer)

    liked = True
    if not like_created:
        like.delete()
        liked = False

    answer.save()
    return JsonResponse({'answer_likes_count': AnswerLike.objects.filter(answer=answer).count(), 'liked': liked})

@require_POST
def helpful_answer(request, answer_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    answer = get_object_or_404(Answer, pk=answer_id)
    if answer.question.author != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    if answer.helpful:
        answer.helpful = False
    else:
        answer.helpful = True

    answer.save()

    return JsonResponse({'helpful': answer.helpful}, status=200)

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
