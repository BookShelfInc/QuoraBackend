"""quora URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

from action.views import TopicAPIView, AnswerAPIView, RegisterAPIView
from app.views import FeedAPIView, UnansweredQuestionsAPIView, BookmarksAPIView, QuestionsByTopicAPIView, \
    AskQuestionAPIView
from info.views import TopicsAPIView
from quora.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', FeedAPIView.as_view()),
    url(r'^unansweredquestions/$', UnansweredQuestionsAPIView.as_view()),
    url(r'^bookmarks/$', BookmarksAPIView.as_view()),
    url(r'^api-token-auth/$', obtain_jwt_token),
    url(r'^profile/', include('info.urls')),
    url(r'^topics/$', TopicsAPIView.as_view()),
    url(r'^topics/(?P<id>[0-9]+)/questions/$', QuestionsByTopicAPIView.as_view()),
    url(r'^ask/$', AskQuestionAPIView.as_view()),
    url(r'^follow/', include('action.urls')),
    url(r'topic/(?P<id>[0-9]+)/$', TopicAPIView.as_view()),
    url(r'^answer/$', AnswerAPIView.as_view()),
    url(r'register/$', RegisterAPIView.as_view()),
]+ static(MEDIA_URL, document_root=MEDIA_ROOT)
