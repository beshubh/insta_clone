from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    message = 'You are not allowed to do this operation';
    def has_object_permisson(self, request, view,obj):
        return obj.user == request.user