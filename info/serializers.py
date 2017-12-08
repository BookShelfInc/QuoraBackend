from rest_framework.fields import IntegerField, CharField
from rest_framework.serializers import ModelSerializer

from action.uploader import uploadImageUser
from app.models import User, Bookmark


class UserSerializer(ModelSerializer):
    count_following = IntegerField(source='following.count')
    count_topics = IntegerField(source='topics.count')
    count_followers = IntegerField(source='followers.count')

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'bio',
                  'count_topics', 'count_following', 'count_followers', 'photo')


class UserProfileChangeSerializer(ModelSerializer):
    username = CharField(required=False, allow_blank=True, initial="current username")

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'bio', 'password', 'photo', 'email',
        )
        write_only_fields = ('password',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def create(self, validated_data):
        user = User(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class CreateBookmarkSerializer(ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('id', 'answer', 'user')

    def create(self, validated_data):
        return Bookmark.objects.create(**validated_data)