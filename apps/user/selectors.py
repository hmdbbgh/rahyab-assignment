from .models import User, Profile


def get_profile(user: User) -> Profile:
    return Profile.objects.get(user=user)
