from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from mailjet_rest import Client

from apps.accounts.models import Account

from .forms import RegistrationForm

mailjet = Client(
    auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY), version="v3.1"
)


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

            # USER ACTIVATION
            current_site = get_current_site(request)

            # Render the email message template with necessary data
            message = render_to_string(
                "accounts/account_verification_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )

            # Prepare the email data
            data = {
                "Messages": [
                    {
                        "From": {"Email": settings.SENDER_EMAIL, "Name": "GreatKart"},
                        "To": [{"Email": email, "Name": f"{first_name} {last_name}"}],
                        "Subject": "Please activate your account",
                        "HTMLPart": message,
                    }
                ]
            }
            # Send the email using the Mailjet API
            mailjet.send.create(data=data)
            return redirect("/accounts/login/?command=verification&email=" + email)
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


def activate(request, uidb64, token):
    try:
        # Decode the uidb64 to get the user's primary key
        uid = urlsafe_base64_decode(uidb64).decode()
        # Retrieve the user based on the primary key
        user = Account._default_manager.get(pk=uid)
    except Exception:
        # If there's an error decoding or retrieving the user, set user to None
        user = None

    # Check if user is not None and the token is valid
    if user is not None and default_token_generator.check_token(user, token):
        # If both conditions are met, activate the user's account
        user.is_active = True
        user.save()
        # Display a success message indicating that the account is activated
        messages.success(request, "Congratulations! Your account is activated.")
        return redirect("login")
    else:
        # If either user is None or the token is invalid, display an error message
        messages.error(request, "Invalid activation link")
        # Redirect the user to the registration page
        return redirect("register")
