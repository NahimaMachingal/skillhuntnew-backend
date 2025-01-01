from rest_framework.permissions import BasePermission

class IsEmployee(BasePermission):
    """
    Custom permission to check if the user is an employee.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and is an employee
        return request.user.is_authenticated and request.user.user_type == 'employee'

class IsJobseeker(BasePermission):
    """
    Custom permission to check if the user is a jobseeker.
    """
    def has_permission(self, request, view):
        # Ensure user is authenticated and a jobseeker
        if not request.user.is_authenticated:
            return False
        print(f"User: {request.user}, User Type: {request.user.user_type}")
        return request.user.user_type == 'jobseeker'

class IsEmployeeOrJobseeker(BasePermission):
    """
    Custom permission to check if the user is either an employee or a jobseeker.
    """
    def has_permission(self, request, view):
        # Ensure user is authenticated and the user type is either employee or jobseeker
        if not request.user.is_authenticated:
            return False
        return request.user.user_type in ['employee', 'jobseeker']
