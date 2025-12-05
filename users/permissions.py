from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    """
    Разрешение: пользователь является модератором.
    Проверяем принадлежность к группе 'moderators'.
    """


    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='moderators').exists()
        )


class IsOwner(BasePermission):
    """
    Разрешение: пользователь является владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsSelf(BasePermission):
    """
    Разрешение: пользователь редактирует ТОЛЬКО свой профиль.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.id == request.user.id
