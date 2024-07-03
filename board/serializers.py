from rest_framework import serializers
from .models import Board, Comment

class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only = True)
    nickname = serializers.ReadOnlyField(source = 'user.nickname')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'nickname', 'comment', 'created_at']

class BoardSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only = True)
    nickname = serializers.ReadOnlyField(source = 'user.nickname')
    class Meta:
        model = Board
        fields = ['id', 'user', 'nickname',  'title', 'created_at']


class BoardDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only = True)
    nickname = serializers.ReadOnlyField(source = 'user.nickname')
    class Meta:
        model = Board
        fields = ['id', 'user', 'nickname', 'title', 'body', 'created_at', 'comments']

class UserPostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = Board
        fields = ['id', 'user', 'title', 'created_at']