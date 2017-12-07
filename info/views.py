# Create your views here.
from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView, ListAPIView, get_object_or_404
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from app.models import User, Topic, Answer, Question
from app.serializers import TopicSerializer, AnswerSerializer, QuestionSerializer
from info.serializers import UserSerializer, UserProfileChangeSerializer


class UserAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TopicsByUserAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TopicSerializer

    def get_queryset(self):
        return Topic.objects.filter(followers__in=self.kwargs['id'])


class FollowingAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(followers__in=self.kwargs['id'])


class FollowersAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(following__in=self.kwargs['id'])


class TopicsAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()


class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class UpdateProfileAPIView(RetrieveAPIView, DestroyModelMixin, UpdateModelMixin):
    permission_classes = (
        permissions.IsAuthenticated,
        UserIsOwnerOrReadOnly,
    )
    serializer_class = UserProfileChangeSerializer

    def get_object(self):
        username = self.kwargs["username"]
        obj = get_object_or_404(User, username=username)
        return obj

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class AnswersByUserAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AnswerSerializer

    def get_queryset(self):
        return Answer.objects.filter(user=self.kwargs['id'])


class QuestionsByUserAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(user=self.kwargs['id'])
