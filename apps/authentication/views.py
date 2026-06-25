import datetime
import jwt
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from apps.user_settings.models import Branch


# Constant credentials
USERNAME = "admin@clinic.com"
PASSWORD = "admin1234"
ROLE = "admin"


def login_view(request):

    branches = Branch.objects.filter(is_active=True)

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        branch_id = request.POST.get("branch_id")

        if email == USERNAME and password == PASSWORD:

            if not branch_id:
                messages.error(request, "Please select a branch.")
                return render(
                    request,
                    "login.html",
                    {"branches": branches}
                )

            payload = {
                "email": email,
                "role": ROLE,
                "branch_id": int(branch_id),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                "iat": datetime.datetime.utcnow(),
            }

            token = jwt.encode(
                payload,
                settings.SECRET_KEY,
                algorithm="HS256"
            )

            response = redirect("home")
            response.set_cookie(
                            "token",
                            token,
                            httponly=True,
                            samesite="Lax"
                        )

            messages.success(request, "Login successful")
            return response

        messages.error(request, "Invalid email or password")

    return render(
        request,
        "login.html",
        {"branches": branches}
    )


def logout_view(request):
    response = redirect("login")
    response.delete_cookie("token")

    return response
