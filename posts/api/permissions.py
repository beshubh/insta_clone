from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    message = 'You should have created this post to update it'
    def has_object_permisson(self, request, view,obj):
        return obj.user == request.user