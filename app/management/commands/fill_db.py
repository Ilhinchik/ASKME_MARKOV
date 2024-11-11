import random
from django.core.management.base import BaseCommand
from app.models import User, Profile, Question, Answer, Tag, QuestionLike, AnswerLike

class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio of entities to generate')

    def handle(self, *args, **options):
        ratio = options['ratio']

        # Создание пользователей
        users = []
        for i in range(ratio):
            # Создаем уникальное имя пользователя
            username = f'user_{i}'
            if User.objects.filter(username=username).exists():
                username = f'user_{i}_{random.randint(1000, 9999)}'  # Добавляем случайный суффикс для уникальности

            user = User.objects.create_user(username=username, password='password')
            Profile.objects.create(user=user)
            users.append(user)

        # Создание тегов
        tags = []
        for i in range(ratio):
            tag_title = f'tag_{i}'
            if not Tag.objects.filter(title=tag_title).exists():
                tag = Tag.objects.create(title=tag_title)
                tags.append(tag)
            else:
                # Если тег с таким названием уже существует, можно использовать его или создать новый с уникальным названием
                tag_title = f'tag_{i}_{random.randint(1000, 9999)}'
                tag = Tag.objects.create(title=tag_title)
                tags.append(tag)

        # Создание вопросов
        questions = []
        for i in range(ratio * 10):
            question = Question.objects.create(
                title=f'Question {i}',
                text='Some question text',
                author=random.choice(users),
            )
            question.tags.set(random.sample(tags, min(3, len(tags))))  # Присваиваем случайные теги
            questions.append(question)

        # Создание ответов
        answers = []
        for i in range(ratio * 100):
            answer = Answer.objects.create(
                question=random.choice(questions),
                text='Some answer text',
                author=random.choice(users)
            )
            answers.append(answer)

        # Создание лайков для вопросов
        for question in questions:
            for user in users:
                # Проверяем, поставил ли пользователь лайк на этот вопрос
                QuestionLike.objects.get_or_create(user=user, question=question)

        # Создание лайков для ответов
        for answer in answers:
            for user in users:
                # Проверяем, поставил ли пользователь лайк на этот ответ
                AnswerLike.objects.get_or_create(user=user, answer=answer)

        self.stdout.write(self.style.SUCCESS('Successfully filled the database'))
