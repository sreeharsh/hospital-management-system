from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test


def role_required(role):
    def check_role(user):
        return user.groups.filter(name=role).exists()

    return user_passes_test(
        check_role,
        login_url="/"
    )