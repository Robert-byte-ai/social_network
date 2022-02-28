from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import ValidationError

from .models import User, Post, Follow, Read


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = (
            'author',
            'pub_date',
            'text',
            'title'
        )
        model = Post


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Follow

    validators = [
        UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=['user', 'following'],
            message='Вы уже подписаны'
        )
    ]

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return data


class ReadSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    class Meta:
        model = Read
        fields = ('user', 'post',)

    def validate(self, data):
        if Read.objects.filter(
            user=data['user'],
            post=data['post']
        ).exists():
            raise ValidationError('Уже прочитано')
        return data
