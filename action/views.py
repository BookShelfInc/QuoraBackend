# Create your views here.
from time import time

from django.http import HttpResponse, JsonResponse
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from app.models import User, Topic
from app.serializers import TopicSerializer, AnswerQuestionSerializer
from info.serializers import UserProfileChangeSerializer

from .dynamoDB import postQuestion

class FollowTopicAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        user = User.objects.get(id=int(request.user.id))
        user.topics.add(int(data['topic']))
        user.save()
        return HttpResponse(status=204)

class FollowUserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        user = User.objects.get(id=int(request.user.id))
        user.following.add(int(data['user']))
        user.save()
        return HttpResponse(status=204)

class TopicAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class AnswerAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        data['user'] = request.user.id
        data['time'] = int(round(time()))
        serializer = AnswerQuestionSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()

            print(serializer.data)

            question_id, answer = serializer.data['question'], serializer.data['content']
            ans_id = serializer.data['id']
            postQuestion(answerId=ans_id, realQuestionId=question_id,
                         answer=answer, userId=request.user.id)

            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class RegisterAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserProfileChangeSerializer