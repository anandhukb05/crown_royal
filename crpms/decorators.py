# decorators.py

import jwt
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse


def jwt_required(view_func):
    def wrapper(request, *args, **kwargs):

        token = request.COOKIES.get("token")

        if not token:
            return redirect("login")

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )

            request.user_data = payload

        except jwt.ExpiredSignatureError:
            return redirect("login")

        except jwt.InvalidTokenError:
            return redirect("login")

        return view_func(request, *args, **kwargs)

    return wrapper


def admin_required(view_func):

    def wrapper(request, *args, **kwargs):

        user = request.user_data

        if user["role"] != "admin":
            return HttpResponse("Access Denied")

        return view_func(request, *args, **kwargs)

    return wrapper