from django.conf.urls import url

from action.views import FollowUserAPIView, FollowTopicAPIView

urlpatterns = [
    url(r'user/$', FollowUserAPIView.as_view()),
    url(r'topic/$', FollowTopicAPIView.as_view()),
]