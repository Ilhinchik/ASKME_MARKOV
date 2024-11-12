import random
from django.core.management.base import BaseCommand
from app.models import User, Profile, Question, Answer, Tag, QuestionLike, AnswerLike


def add_users(ratio):
    User.objects.create_superuser("ilha", "ilha@root.com", "ilha")

    for i in range(ratio):
        user = User.objects.create_user(f"user{i}", f"user{i}@user.com", f"user{i}")
        Profile.objects.create(user=user, avatar='static/images/image.webp')

    print("Пользователи созданы")


def add_tags(ratio):
    for i in range(ratio):
        Tag.objects.create(
            title = f'tag{i}'
        )
    print("Тэги созданы")


def add_questions(ratio, users, tags):
    questions = []
    for i in range(ratio * 10):
        question = Question.objects.create(
            title=f'Question {i}?',
            text='Some question text',
            author=random.choice(users)
        )
        question.tags.set(random.sample(tags, random.randint(2, min(5, len(tags)))))
        questions.append(question)
    print("Вопросы созданы")
    return questions


def add_answers(ratio, users, questions):
    answers = []
    for i in range(ratio * 100):
        answer = Answer.objects.create(
            question=random.choice(questions),
            text='Some answer text.',
            author=random.choice(users)
        )
        answers.append(answer)
    print("Ответы созданы")
    return answers


def add_question_likes(ratio, users, questions):
    question_likes_count = ratio * 200 // 2
    for _ in range(question_likes_count):
        user = random.choice(users)
        question = random.choice(questions)
        QuestionLike.objects.get_or_create(user=user, question=question)
    print("Лайки для вопросов созданы")


def add_answer_likes(ratio, users, answers):
    answer_likes_count = ratio * 200 - (ratio * 200 // 2)
    for _ in range(answer_likes_count):
        user = random.choice(users)
        answer = random.choice(answers)
        AnswerLike.objects.get_or_create(user=user, answer=answer)
    print("Лайки для ответов созданы")




class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio of entities to generate')

    def handle(self, *args, **options):
        ratio = options['ratio']

        add_users(ratio)
        users = list(User.objects.all())

        add_tags(ratio)
        tags = list(Tag.objects.all())

        questions = add_questions(ratio, users, tags)
        answers = add_answers(ratio, users, questions)

        add_question_likes(ratio, users, questions)
        add_answer_likes(ratio, users, answers)

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена'))