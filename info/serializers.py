from rest_framework.fields import IntegerField, CharField
from rest_framework.serializers import ModelSerializer

from app.models import User


class UserSerializer(ModelSerializer):
    count_following = IntegerField(source='following.count')
    count_topics = IntegerField(source='topics.count')
    count_followers = IntegerField(source='followers.count')

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'bio', 'avatar',
                  'count_topics', 'count_following', 'count_followers')


class UserProfileChangeSerializer(ModelSerializer):
    username = CharField(required=False, allow_blank=True, initial="current username")

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'bio', 'password',
        )

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
