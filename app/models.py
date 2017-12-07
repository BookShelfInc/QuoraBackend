from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import ManyToManyField, Model, TextField, PositiveIntegerField, ForeignKey, ImageField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.

class Topic(Model):
    title = TextField()
    picture = ImageField(upload_to='images/', )
    description = TextField()

    def __str__(self):
        return self.title


class User(AbstractUser):
    avatar = ImageField(upload_to='images/', null=True, blank=True)
    following = ManyToManyField('self', related_name='followers', blank=True, symmetrical=False)
    topics = ManyToManyField(Topic, related_name='followers', )
    bio = TextField(null=True, blank=True)


class Vote(Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    user = ForeignKey(User, on_delete=models.CASCADE, )

    class Meta:
        unique_together = (('user', 'content_type', 'object_id'),)


class Question(Model):
    time = PositiveIntegerField()
    topic = ForeignKey(Topic, on_delete=models.CASCADE, )
    content = TextField()
    user = ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-id"]


class Answer(Model):
    content = TextField()
    user = ForeignKey(User, on_delete=models.CASCADE, )
    time = PositiveIntegerField()
    question = ForeignKey(Question, on_delete=models.CASCADE, )


class Commentary(Model):
    user = ForeignKey(User, on_delete=models.CASCADE, )
    answer = ForeignKey(Answer, on_delete=models.CASCADE, )
    time = PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Commentaries'


class Bookmark(Model):
    user = ForeignKey(User, on_delete=models.CASCADE, )
    answer = ForeignKey(Answer, on_delete=models.CASCADE, )
