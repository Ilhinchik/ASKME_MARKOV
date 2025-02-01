"""
URL configuration for askme_markov project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='question'),
    path('tag/<str:tag_title>', views.tag, name='tag'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('question_like/<int:question_id>/', views.question_like, name='question_like'),
    path('answer_like/<int:answer_id>/', views.answer_like, name='answer_like'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('helpful_answer/<int:answer_id>/', views.helpful_answer, name='helpful_answer'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)