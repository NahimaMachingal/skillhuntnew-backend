# api/permissions.py
from rest_framework.permissions import BasePermission

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'employee'

class IsJobseeker(BasePermission):
    def has_permission(self, request, view):
        print(f"User: {request.user}, User Type: {request.user.user_type}")
        return request.user.user_type == 'jobseeker'
