from rest_framework import serializers
from xfzauth.serializers import UserSerializer
from .models import News, NewsCategory, Comment, Banner


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('pk', 'name')


class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer()
    author = UserSerializer()

    class Meta:
        model = News
        fields = ('pk', 'title', 'desc', 'thumbnail', 'pub_time', 'category',
                  'author')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = ('pk', 'content', 'author', 'pub_time')


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['pk', 'image_url', 'priority', 'link_to']
