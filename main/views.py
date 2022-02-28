from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters
from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User, Post, Follow, Read
from .serializers import (
    UserRegisterSerializer,
    PostSerializer,
    FollowSerializer,
    ReadSerializer
)
from .filters import PostFilter
from .pagination import PostsPagination
from .mixins import CreateListMixins, DestroyCreateMixins


class UserViewSet(CreateListMixins):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('posts_count',)

    def get_queryset(self):
        queryset = User.objects.all()
        if 'posts_count' in self.request.query_params.get('ordering'):
            queryset = queryset.annotate(posts_count=Count('posts'))
        return queryset


class PostViewSet(CreateListMixins):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = PostFilter
    ordering = ('pub_date',)
    pagination_class = PostsPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['POST'], detail=True)
    def read(self, request, pk):
        data = {'user': request.user.id, 'post': pk}
        serializer = ReadSerializer(
            data=data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors)

    @read.mapping.delete
    def delete_read(self, request, pk):
        read = get_object_or_404(
            Read,
            user=request.user,
            post=get_object_or_404(Post, id=pk)
        )
        read.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(DestroyCreateMixins):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
