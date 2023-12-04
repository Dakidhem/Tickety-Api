from rest_framework import permissions

class IsFRAssistant(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST']:
            return request.user.role == 'FR_ASSISTANT'
        return True
    
class IsDzAssistant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'DZ_ASSISTANT'

from rest_framework import permissions

class IsTicketOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read permissions for anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow write permissions only if the user is the assigned_to or created_by
        return obj.assigned_to == request.user or obj.created_by == request.user