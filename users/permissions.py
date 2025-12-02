from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    """
    Разрешение: пользователь является модератором.
    Проверяем принадлежность к группе 'moderators'.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.groups.filter(name='moderators').exists()
        )
