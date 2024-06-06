from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
  """Permission to allow only admin users to create/update/delete"""
  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
      return True
    return request.user.is_staff
