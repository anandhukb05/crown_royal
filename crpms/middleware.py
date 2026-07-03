# middleware.py

import jwt
from django.shortcuts import redirect
from django.conf import settings


class JWTMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        public_prefixes = ["/login/", "/static/", "/logout/"]
        public_exact = ["/"]

        if request.path in public_exact or any(
            request.path.startswith(p) for p in public_prefixes
        ):
            return self.get_response(request)

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
            request.branch_id = payload.get("branch_id")

        except jwt.ExpiredSignatureError:
            return redirect("login")
        except jwt.InvalidTokenError:
            return redirect("login")

        return self.get_response(request)
