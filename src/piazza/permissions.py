from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from .models import Post


class CommentLikePerm(permissions.BasePermission):
    message = "You do not have permission because this post is expired."

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        #
        if view.action == 'comments':
            post_obj = get_object_or_404(Post, id=view.kwargs.get('pk'))
            if post_obj.has_expired:

                if request.method not in SAFE_METHODS:
                    return False
            if post_obj.set_status() != Post.ACTIVE:

                if request.method not in SAFE_METHODS:

                    self.message = "You do not have permission, this post is no longer ACTIVE."
                    return False
        return True

    def has_object_permission(self, request, view, obj):

        if view.action == 'like':
            if obj.has_expired:
                return False
            if request.user == obj.owner:
                self.message = 'You cannot Like your own post'
                return False
            if obj.set_status() != Post.ACTIVE:
                self.message = "You do not have permission, this post is no longer ACTIVE."
                return False
        elif view.action == 'dislike':
            if obj.has_expired:
                return False
            if request.user == obj.owner:
                self.message = 'You cannot Dislike your own post'
                return False
            if obj.set_status() != Post.ACTIVE:
                self.message = "You do not have permission, this post is no longer ACTIVE."
                return False

        return True
