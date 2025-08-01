from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode

User = get_user_model()

# Sign Up View
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        age = request.POST['age']
        gender = request.POST['gender']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            age=age,
            gender=gender
        )
        messages.success(request, 'Account created successfully.')
        return redirect('signin')
    return render(request, 'signup.html')

# Sign In View
def signin_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Change this to your home page view name
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'signin.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('signin')

# Forgot Password View
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(f"/accounts/reset-password/{uid}/{token}/")

            # Send email
            send_mail(
                'Password Reset',
                f'Hi {user.username},\n\n'
                f'You requested a password reset. Click the link below to reset your password:\n\n'
                f'{reset_link}\n\n'
                f'If you didn’t request this, you can ignore this email.',
                'your_email@example.com',
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Password reset email sent.')
        else:
            messages.error(request, 'Email not found.')
    return render(request, 'forgot_password.html')


def reset_password_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successful. Please sign in.')
                return redirect('signin')
            else:
                messages.error(request, 'Passwords do not match.')
        return render(request, 'reset_password.html', {'validlink': True})
    else:
        messages.error(request, 'Invalid or expired password reset link.')
        return render(request, 'reset_password.html', {'validlink': False})