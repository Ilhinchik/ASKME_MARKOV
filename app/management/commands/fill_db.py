import random
from django.core.management.base import BaseCommand
from app.models import User, Profile, Question, Answer, Tag, QuestionLike, AnswerLike


def add_users(ratio):
    User.objects.create_superuser("ilha", "ilha@root.com", "ilha")

    users = [User(username=f"user{i}", email=f"user{i}@user.com") for i in range(ratio)]
    User.objects.bulk_create(users) 

    profiles = [Profile(user=user, avatar='static/images/image.webp') for user in User.objects.filter(username__startswith="user")]
    Profile.objects.bulk_create(profiles)

    print("Пользователи созданы")


def add_tags(ratio):
    tags = [Tag(title=f'tag{i}') for i in range(ratio)]
    Tag.objects.bulk_create(tags)  
    print("Тэги созданы")


def add_questions(ratio, users, tags):
    questions = [
        Question(
            title=f'Question {i}?',
            text='Some question text',
            author=random.choice(users)
        ) for i in range(ratio * 10)
    ]
    Question.objects.bulk_create(questions)

    questions = list(Question.objects.all())
    for question in questions:
        question.tags.set(random.sample(tags, random.randint(2, min(5, len(tags)))))

    print("Вопросы созданы")
    return questions


def add_answers(ratio, users, questions):
    answers = [
        Answer(
            question=random.choice(questions),
            text='Some answer text.',
            author=random.choice(users)
        ) for i in range(ratio * 100)
    ]
    Answer.objects.bulk_create(answers) 
    print("Ответы созданы")
    return answers


def add_question_likes(ratio, users, questions):
    question_likes = [
        QuestionLike(user=random.choice(users), question=random.choice(questions))
        for _ in range(ratio * 200 // 2)
    ]
    QuestionLike.objects.bulk_create(question_likes, ignore_conflicts=True) 
    print("Лайки для вопросов созданы")


def add_answer_likes(ratio, users, answers):
    answer_likes = [
        AnswerLike(user=random.choice(users), answer=random.choice(answers))
        for _ in range(ratio * 200 - (ratio * 200 // 2))
    ]
    AnswerLike.objects.bulk_create(answer_likes, ignore_conflicts=True)
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
