import requests
from django.contrib.auth import logout,login


from asosiy.settings import EMAIL_HOST_USER
from user.forms import UserForm


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})


from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('course-list')
        else:
            error = "Login yoki parol noto‘g‘ri"
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('course-list')




from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils.timezone import now, timedelta
from django.http import JsonResponse, HttpResponse
from django.views import View

User = get_user_model()

class UserStatsView(View):
    def get(self, request):
        total_users = User.objects.count()
        roles = User.objects.values('role').annotate(count=Count('role'))


        today = now().date()
        last_7_days = [
            {
                'date': (today - timedelta(days=i)).isoformat(),
                'count': User.objects.filter(date_joined__date=today - timedelta(days=i)).count()
            }
            for i in range(30)
        ]
        last_7_days.reverse()  # Qadimgidan yangigacha tartiblash

        return JsonResponse({
            'total_users': total_users,
            'roles': list(roles),
            'last_7_days': last_7_days
        })


from django.shortcuts import render

def user_stats_page(request):
    return render(request, 'user_stats.html')




from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import render_to_string
from .forms import ContactAdminForm

@login_required
def contact_admin(request):
    user = request.user
    user_email = user.email
    if request.method == 'POST':
        form = ContactAdminForm(request.POST, user_email=user_email)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            context = {
                'username': user.username,
                'email': user.email,
                'message': message
            }

            html_message = render_to_string('user_to_admin.html', context)
            text_message = f"Username: {user.username}\nEmail: {user.email}\n\nXabar:\n{message}"

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[settings.EMAIL_HOST_USER],
            )
            email.attach_alternative(html_message, "text/html")
            email.send()

            return render(request, 'success.html', {'email': user_email})
    else:
        form = ContactAdminForm(user_email=user_email)

    return render(request, 'contact_admin.html', {'form': form})


# parolni tiklash uchun viewlar
import random
import uuid
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import PasswordResetRequest, CustomUser

User = get_user_model()


# 1. Kod yuboruvchi view
def send_reset_code_view(request):
    if request.method == 'POST':
        login = request.POST.get('login')

        try:
            user = User.objects.get(username=login)
        except User.DoesNotExist:
            return render(request, 'password_reset/request_invalid.html', {'error': 'Login topilmadi.'})

        # 6 xonali tasodifiy kod yaratish
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        # Reset token bilan saqlash (avtomatik vaqt tekshiruvi modelda bo‘ladi)
        reset_request = PasswordResetRequest.objects.create(user=user, code=code)

        # To'g'ri lokal havola
        reset_link = f"http://o-quvmarkaz-roa0.onrender.com/reset-password/{reset_request.token}/"

        # Email yuborish
        send_mail(
            subject="Parolni tiklash uchun kod",
            message=(
                f"Salom {user.username},\n\n"
                f"Siz parolni tiklashni so‘radingiz.\n"
                f"6 xonali tasdiqlash kodingiz: {code}\n"
                f"Parolni yangilash uchun ushbu havolani oching:\n{reset_link}\n\n"
                f"Agar bu siz bo‘lmasangiz, bu xabarni e'tiborsiz qoldiring."
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email,EMAIL_HOST_USER],
            fail_silently=False
        )

        return render(request, 'password_reset/code_sent.html')

    return render(request, 'password_reset/request_form.html')


# 2. Kodni tekshirish va parolni yangilovchi view
def reset_password_view(request, token):
    try:
        reset_request = PasswordResetRequest.objects.get(token=token)
    except PasswordResetRequest.DoesNotExist:
        return render(request, 'password_reset/invalid_token.html')

    # Kod muddati o‘tganini tekshirish (modeldagi .is_valid() metod orqali)
    if not reset_request.is_valid():
        return render(request, 'password_reset/expired.html')

    if request.method == 'POST':
        code = request.POST.get('code')
        new_password = request.POST.get('new_password')

        if reset_request.code == code:
            user = reset_request.user
            user.set_password(new_password)
            user.save()

            # Bu tokenni va kodni o‘chirish (yana ishlatilmasligi uchun)
            reset_request.delete()

            return redirect('login')  # login sahifangiz url nomi shu bo‘lsa

        else:
            return render(request, 'password_reset/new_password.html', {
                'error': 'Kod noto‘g‘ri!',
                'token': token
            })

    return render(request, 'password_reset/new_password.html', {'token': token})


def google_login(request):
    auth_url = (
        f"{settings.GOOGLE_AUTH_URL}"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
    )
    return redirect(auth_url)


def google_callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("Kod yo‘q", status=400)

    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_response = requests.post(settings.GOOGLE_TOKEN_URL, data=token_data)

    if token_response.status_code != 200:
        return HttpResponse(f"Access token olinmadi: {token_response.text}", status=400)

    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return HttpResponse("Access token olinmadi", status=400)

    user_info_response = requests.get(
        settings.GOOGLE_USER_INFO_URL,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    if user_info_response.status_code != 200:
        return HttpResponse("Foydalanuvchi ma'lumotlari olinmadi", status=400)

    user_info = user_info_response.json()
    email = user_info.get("email")
    if not email:
        return HttpResponse("Email olinmadi", status=400)

    user, created = CustomUser.objects.get_or_create(email=email)
    if created:
        user.username = user_info.get("given_name") or email.split("@")[0]
        user.save()

    login(request, user)
    return redirect('course-list')

#profile
from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def profile_detail(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    return render(request, 'profile/profile_detail.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile/profile_edit.html', {'form': form})


