from django.db.models import OuterRef, Count, Subquery, F
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Like, Dislike, Post, Comment
from .permissions import CommentLikePerm
from .serializers import PostSerializer, CommentSerializer
from .utils import PostFilter


class PostViewSet(ModelViewSet):
    likes_qs = Like.objects.filter(post=OuterRef('pk')).annotate(no_likes=Count('users')).values('no_likes')
    dislikes_qs = Dislike.objects.filter(post=OuterRef('pk')).annotate(no_dislikes=Count('users')).values('no_dislikes')
    # using a subquery to get the number of likes and dislikes
    queryset = Post.objects.annotate(
        like_count=Subquery(likes_qs.values('no_likes'))
    ).annotate(
        dislike_count=Subquery(dislikes_qs.values('no_dislikes'))
    ).annotate(activity_count=F('like_count')+F('dislike_count')) # .order_by('-like_count', '-dislike_count')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, CommentLikePerm]
    # Using django-filter classes
    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
    ordering_fields = ['like_count', 'dislike_count', 'activity_count']

    search_fields = ['title']
    # custom filter classes
    filterset_class = PostFilter

    @action(detail=True)
    def like(self, request, pk=None):
        post = self.get_object()

        # create likes table if it doesn't exist
        try:
            post.likes
        except Post.likes.RelatedObjectDoesNotExist as identifier:
            Like.objects.create(post=post)

        # create dislikes table if it doesn't exist
        try:
            post.dis_likes
        except Post.dis_likes.RelatedObjectDoesNotExist as identifier:
            Dislike.objects.create(post=post)

        if request.user in post.likes.users.all():
            post.likes.users.remove(request.user)
        else:
            post.likes.users.add(request.user)
            post.dis_likes.users.remove(request.user)

        res = {
            "user": {
                "username": request.user.username,
            },
            "action": "like",
            "expiry_duration": post.expiry_duration()

        }

        return Response(res)

    @action(detail=True)
    def dislike(self, request, pk=None):
        post = self.get_object()

        try:
            post.likes
        except Post.likes.RelatedObjectDoesNotExist as identifier:
            Like.objects.create(post=post)

        try:
            post.dis_likes
        except Post.dis_likes.RelatedObjectDoesNotExist as identifier:
            Dislike.objects.create(post=post)

        if request.user in post.dis_likes.users.all():
            post.dis_likes.users.remove(request.user)
        else:
            post.dis_likes.users.add(request.user)
            post.likes.users.remove(request.user)

        res = {
            "user": {
                "username": request.user.username,
            },
            "action": "dislike",
            "expiry_duration": post.expiry_duration()
        }

        return Response(res)

    @action(detail=False, methods=['POST', 'GET'])
    def comments(self, request, pk):
        post = self.get_object()
        self.serializer_class = CommentSerializer
        qs = Comment.objects.filter(post=post)
        if request.method == 'GET':

            serializer = self.serializer_class(
                qs, many=True, context={'request': request}
            )
            return Response(serializer.data)
        else:
            serializer = self.serializer_class(
                data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True) # validate data before saving
            serializer.save(owner=request.user, post=post)
            return Response(serializer.data)
