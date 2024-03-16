from rest_framework import permissions

class IsApplicant(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.role == 'applicant' or request.user.is_staff)

class IsRecruiter(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.role == 'recruiter'or request.user.is_staff)
    
