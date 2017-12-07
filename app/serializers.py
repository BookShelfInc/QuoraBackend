from rest_framework.serializers import ModelSerializer
from app.models import Question, Topic, Bookmark, Answer


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'title',)


class QuestionSerializer(ModelSerializer):
    topic = TopicSerializer()

    class Meta:
        model = Question
        fields = ('id', 'time', 'topic', 'content',)


class AnswerSerializer(ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = ('id', 'content', 'question',)


class BookmarkSerializer(ModelSerializer):
    answer = AnswerSerializer()
    class Meta:
        model = Bookmark
        fields = ('id', 'answer',)

class QuestionCreateSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'time', 'topic', 'content', 'user')

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

class AnswerQuestionSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'time', 'content', 'question', 'user')

        def create(self, validated_data):
            return Answer.objects.create(**validated_data)