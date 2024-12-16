# from rest_framework import permissions

# class IsManager(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.user and (request.user.is_staff or request.user.is_superuser))

# class IsAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_superuser)
    

from rest_framework import permissions
from .getUserBySession import getUserBySession

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        user = getUserBySession(request)
        return bool(user and (user.is_staff or user.is_superuser))

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = getUserBySession(request)
        return bool(user and user.is_superuser)
    
class IsAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        user = getUserBySession(request)
        print(f"User in permission check: {user}")
        return bool(user)

    

    