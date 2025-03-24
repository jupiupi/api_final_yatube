from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Post, Group, Follow

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "title", "slug", "description")
        model = Group
        read_only_fields = ("id",)


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ("id", "author", "text", "pub_date", "image", "group")
        model = Post
        read_only_fields = ("id", "author", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ("id", "author", "text", "created", "post")
        model = Comment
        read_only_fields = ("id", "author", "created", "post")


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all(),
    )

    class Meta:
        model = Follow
        fields = ("user", "following")
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Подписка на автора оформлена ранее!'
            ),
        )

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return data
