from users.models import User

__all__ = ("Users",)


class Users:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user = User.objects.get(pk=request.user.pk)
        return self.get_response(request)
