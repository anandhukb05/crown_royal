# middleware.py

import jwt
from django.shortcuts import redirect
from django.conf import settings


class JWTMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print("Path:", request.path)

        public_urls = ["/login/", "/static/", "/", "/logout/"]

        if any(request.path.startswith(url) for url in public_urls):
            print("Public URL")
            return self.get_response(request)

        token = request.COOKIES.get("token")
        print("Token:", token)

        if not token:
            print("No token")
            return redirect("login")

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )

            request.user_data = payload
            print("Valid token")

        except Exception as e:
            print("JWT Error:", e)
            return redirect("login")

        return self.get_response(request)