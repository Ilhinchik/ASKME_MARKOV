from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CharField, PasswordInput, ModelForm

from app.models import Profile, Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )
    confirm = forms.BooleanField(widget=forms.CheckboxInput)

    def clean_username(self):
        return self.cleaned_data['username'].strip()
    

class UserForm(forms.ModelForm):

    password_confirmation = CharField(widget=PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {
            'password': PasswordInput(),
        }

    def clean(self):
        data = super().clean()

        if data['password'] != data['password_confirmation']:
            raise ValidationError('Passwords do not match')

        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()

        return user

class ProfileEditForm(forms.ModelForm):

    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = Profile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance').user if 'instance' in kwargs else None
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        # Предзаполнение полей пользователя
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        # Сохраняем данные профиля
        profile = super().save(commit=False)
        if commit:
            profile.save()

        # Обновляем данные пользователя (email и username)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.save()

        return profile

class QuestionAskForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Введите через запятую")
    class Meta:
        model = Question
        fields=['title', 'text', 'tags']

class AnswerForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control my-3', 'placeholder': 'Enter your answer here', 'rows': '5'}),
    )

    class Meta:
        model = Answer
        fields = ['text']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.question_id = kwargs.pop('question_id', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        question = Question.objects.get(pk=self.question_id)
        answer = Answer(author=self.user, question=question, text=self.cleaned_data.get('text'))
        if commit:
            answer.save()
        return answer
