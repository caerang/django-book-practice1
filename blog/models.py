import re
from django import forms
from django.db import models
from django.conf import settings


def lnglat_validator(value):
    if not re.match(r'^[+-]?\d+\.?\d*, [+-]?\d+\.?\d*', value):
        raise forms.ValidationError('경도위도를 입력해 주세요')

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    photo = models.ImageField()
    lnglat = models.CharField(max_length=40, blank=True, validators=[lnglat_validator])
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def lng(self):
        if self.lnglat:
            return self.lnglat.split(',')[0]
        return None

    @property
    def lat(self):
        if self.lnglat:
            return self.lnglat.split(',')[1]
        return None


class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
