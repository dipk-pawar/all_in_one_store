from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.accounts.models import Account

from .forms import RegistrationForm


# Create your views here.
def register_user(request):
    # Handle registration form submission
    if request.method == "POST":
        # Validate form data
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            # Derive username from email
            username = email.split("@")[0]
            # Create a new user account
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            # Add additional user details
            user.phone_number = phone_number
            user.save()
            # Display success message
            messages.success(request, "Registration successfully")
            return redirect("register")
    else:
        # If request method is not POST, display empty registration form
        form = RegistrationForm()
    context = {"form": form}
    # Render registration page with form
    return render(request, "accounts/register.html", context)


def login_user(request):
    # Handle user login
    if request.method == "POST":
        # Get email and password from request
        email = request.POST["email"]
        password = request.POST["password"]

        # Validate email and password
        if email.strip() == "" or password.strip == "":
            messages.error(request, "Please enter the required field")
            return redirect("login")
        # Authenticate user
        user = auth.authenticate(email=email, password=password)
        # Check if authentication was successful
        if user is not None:
            # Log in the user
            auth.login(request, user)
            # Redirect to home page
            return redirect("home")
        # Display error message for invalid credentials
        messages.error(request, "Invalid credentials")
    # Render login page
    return render(request, "accounts/login.html")


@login_required(login_url="login")
def logout_user(request):
    # Log out the user
    auth.logout(request)
    # Display success message
    messages.success(request, "You are successfully logged out")
    # Redirect to login page
    return redirect("login")
