from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count

class QuestionManager(models.Manager):
    def newest(self):
        return self.order_by('-created_at')

    def hot(self):
        return self.annotate(likes_count=Count('questionlike')).order_by('-likes_count')
    


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title



class Question(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag)

    objects = QuestionManager()

    def likes_count(self):
        # Получает количество лайков для вопроса, считая записи в QuestionLike
        return self.questionlike_set.count()

    def __str__(self):
        return self.title
    

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def likes_count(self):
        return self.answerlike_set.count()
    
    def __str__(self):
        return f"Answer by {self.author} {self.id} on {self.question.title}"




class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')



class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'answer')



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
