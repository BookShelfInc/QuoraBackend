# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView, ListAPIView, get_object_or_404, CreateAPIView
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated

from action.uploader import uploadImageUser
from action.avatar_crop_api import cropImage
from action.env_getter import getVariable
from app.models import User, Topic, Answer, Question, Bookmark
from app.serializers import TopicSerializer, AnswerSerializer, QuestionSerializer
from info.serializers import UserSerializer, UserProfileChangeSerializer, CreateBookmarkSerializer


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


@api_view(['POST',])
@csrf_exempt
@permission_classes([IsAuthenticated, ])
def uploadImage(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            photo_path = uploadImageUser(request.FILES['image'])
            imageName = photo_path.replace(getVariable('s3BucketPath'), '')
            photo_small_path = getVariable('s3BucketPath') + cropImage(imageName)[1:-1]

            user = request.user
            user.photo = photo_small_path
            user.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)
    return HttpResponse(status=400)


class QuestionsByUserAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(user=self.kwargs['id'])

class CreateBookmarkAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        data['user'] = request.user.id
        serializer = CreateBookmarkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)