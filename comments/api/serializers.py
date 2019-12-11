from rest_framework.serializers import ModelSerializer,SerializerMethodField
from comments.models import Comment

class CommentsSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'post',
            'user',
            'text',
            'timestamp',
        ]