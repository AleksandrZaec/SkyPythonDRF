from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Пользователь может редактировать и удалять только свои объекты.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем GET, HEAD, OPTIONS запросы без проверки владельца
        if request.method in SAFE_METHODS:
            return True

        # Разрешаем редактирование и удаление только владельцу объекта
        return obj.owner == request.user


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Модераторы').exists()


class IsModeratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='Модераторы').exists():
            return view.action in ['retrieve', 'update', 'partial_update', 'list']
        return request.method in SAFE_METHODS


class IsOwnerOrModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.groups.filter(name='Модераторы').exists():
            return True
        return obj.owner == request.user
