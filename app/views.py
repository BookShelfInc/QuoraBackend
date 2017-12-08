# Create your views here.
from django.http import JsonResponse
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated

from app.models import Question, Bookmark
from app.paginations import FeedPagination
from app.serializers import QuestionSerializer, BookmarkSerializer, QuestionCreateSerializer
import time


class FeedAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Question.objects.all()
    pagination_class = FeedPagination
    serializer_class = QuestionSerializer


class UnansweredQuestionsAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Question.objects.filter(answer=None)
    pagination_class = FeedPagination
    serializer_class = QuestionSerializer


class BookmarksAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = FeedPagination
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)


class QuestionsByTopicAPIView(ListAPIView):
    pagination_class = FeedPagination
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(topic_id=self.kwargs['id'])


class AskQuestionAPIView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        data['user'] = request.user.id
        data['time'] = int(round(time.time()))
        serializer = QuestionCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
