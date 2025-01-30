from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count


class TagManager(models.Manager):
    def popular(self):
        return self.annotate(question_count=Count('questions')).order_by('question_count')[:10]

class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)

    objects = TagManager()

    def __str__(self):
        return self.title

class QuestionManager(models.Manager):
    def newest(self):
        return self.order_by('-created_at')

    def hot(self):
        return self.annotate(likes_count=Count('likes')).order_by('-likes_count')

    def tagged(self, tag_name):
        return self.filter(tags__title=tag_name).order_by('-created_at')


class Question(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name="questions")

    objects = QuestionManager()

    def likes_count(self):
        return self.likes.count()

    def ans_count(self):
        return self.answers.count()

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')

    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return f"Answer by {self.author} on {self.question.title}"


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'question')


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'answer')


class ProfileManager(models.Manager):
    def get_top_users(self):
        return self.select_related('user').annotate(answer_count=Count('user__answers')).order_by('-answer_count')[:5]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = ProfileManager()


    def __str__(self):
        return f"Profile of {self.user.username}"
