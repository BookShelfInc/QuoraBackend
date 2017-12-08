from django.conf.urls import url

from info.views import UserAPIView, TopicsByUserAPIView, FollowingAPIView, \
    FollowersAPIView, UpdateProfileAPIView, AnswersByUserAPIView, QuestionsByUserAPIView, \
    uploadImage, CreateBookmarkAPIView

urlpatterns = [
    url(r'(?P<id>[0-9]+)/$', UserAPIView.as_view()),
    url(r'(?P<id>[0-9]+)/topics/$', TopicsByUserAPIView.as_view()),
    url(r'(?P<id>[0-9]+)/following/$', FollowingAPIView.as_view()),
    url(r'(?P<id>[0-9]+)/followers/$', FollowersAPIView.as_view()),
    # url(r'change/(?P<username>[\w-]+)$', UpdateProfileAPIView.as_view()),
    url(r'(?P<id>[0-9]+)/answers/$', AnswersByUserAPIView.as_view()),
    url(r'(?P<id>[0-9]+)/questions/$', QuestionsByUserAPIView.as_view()),
    url(r'change/image/$', uploadImage),
    url(r'bookmark/$', CreateBookmarkAPIView.as_view()),
]
