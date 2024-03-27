from django.contrib.auth.backends import ModelBackend

from .models import Profile


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Profile.objects.get(username__exact=username)
        except Profile.DoesNotExist:
            # No user was found, return None
            return None
        else:
            if user.check_password(password):
                # Password verified, return the user
                return user
            else:
                # Incorrect password, return None
                return None

    def get_user(self, user_id):
        try:
            return Profile.objects.get(pk=user_id)
        except Profile.DoesNotExist:
            return None
