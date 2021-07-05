from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Post, Comment

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'message', 'owner']
        read_only_fields = ['owner']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user_id = ret.pop('owner', None)
        user_obj = User.objects.filter(id=user_id).first()
        extra_ret = {
            "post_id": instance.post.id,
            "action": "comment",
            "author": {
                "username": user_obj.username,
            },

        }
        ret.update(extra_ret)
        return ret


class PostSerializer(serializers.ModelSerializer):
    expired = serializers.ReadOnlyField(source='has_expired')
    expires_in = serializers.ReadOnlyField(source='expiry_duration')
    like_count = serializers.IntegerField(read_only=True)
    dislike_count = serializers.IntegerField(read_only=True)
    status = serializers.ReadOnlyField(source='set_status')
    activity_count = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['owner']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)

    # formatting the returned json
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user_id = ret.pop('owner', None)
        if ret.get('like_count') is None:
            # setting likes, dislike, activity_count to 0 if returned as null
            ret.update({
                'like_count': 0,
                'dislike_count': 0,
                'activity_count': 0
            })

        user_obj = User.objects.filter(id=user_id).first()
        extra_ret = {
            "author": {
                "username": user_obj.username,
            },

        }

        ret.update(extra_ret)
        return ret
