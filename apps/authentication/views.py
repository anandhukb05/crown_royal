import datetime
import jwt
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

# Constant credentials
USERNAME = "admin@clinic.com"
PASSWORD = "admin1234"

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")       # matches HTML field name="email"
        password = request.POST.get("password") # matches HTML field name="password"

        if email == USERNAME and password == PASSWORD:
            payload = {
                "email": email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                "iat": datetime.datetime.utcnow(),
            }

            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

            request.session["jwt_token"] = token

            messages.success(request, "Login successful")
            return redirect("home")

        else:
            messages.error(request, "Invalid email or password")

    return render(request, "login.html")