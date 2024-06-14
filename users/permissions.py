from rest_framework import permissions


class IsModeratorOrOwner(permissions.BasePermission):
    """
    Разрешение, позволяющее доступ только владельцам объекта или модераторам.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_staff
