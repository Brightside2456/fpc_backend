from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self, request, username = ..., password = ..., **kwargs):
        custom_user_model = get_user_model()
        try:
            user = custom_user_model.objects.get(email=username)
        except custom_user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
    