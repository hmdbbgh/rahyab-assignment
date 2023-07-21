from django.db import transaction
from .models import User, Profile


def create_profile(
    *,
    user: User,
    bio: str | None
) -> Profile:
    return Profile.objects.create(user=user, bio=bio)


def create_user(
    *,
    username: str,
    email: str,
    password: str,
    **extra_fields
) -> User:
    return User.objects.create_user(
        email=email,
        username=username,
        password=password,
        **extra_fields
    )


@transaction.atomic
def register(
    *,
    email: str,
    username: str,
    password: str,
    bio: str | None,
    first_name: str | None,
    last_name: str | None,
) -> User:
    user = create_user(
        email=email,
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    create_profile(user=user, bio=bio)

    return user
