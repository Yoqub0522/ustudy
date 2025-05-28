from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect

from asosiy.settings import EMAIL_HOST_USER
from user.models import Role


def checking_user(func):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return func(request,*args,**kwargs)
    return wrapper

def checking_role(func):
    def wrapper(request,*args,**kwargs):
        if  request.user.is_authenticated:
            if request.user.role==Role.ADMIN:
               return func(request,*args,**kwargs)
            else:
                raise PermissionError

        else:
            raise PermissionError
    return wrapper


def send_message(request):
    send_mail(
        subject="savollar",
        message='salom',
        from_email=EMAIL_HOST_USER,
        recipient_list=[EMAIL_HOST_USER, 'abdullagulomjonov2306@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse('yuborildi')

xabar ="""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Yangi Kurslar Reklamasi</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f8f9fa; padding: 20px;">
    <div style="max-width: 600px; margin: auto; background-color: white; border-radius: 8px; padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <h2 style="text-align: center; color: #343a40;">🎓 O'quv Markazida Yangi Kurslar!</h2>
        <p style="font-size: 16px;">Assalomu alaykum hurmatli foydalanuvchi!</p>
        <p style="font-size: 16px;">Bizning o‘quv markazimizda yangi va zamonaviy kurslar uchun ro‘yxatga olish boshlandi. Quyidagilarni taklif qilamiz:</p>
        <ul style="font-size: 16px;">
            <li>✅ Python va Django dasturlash kurslari</li>
            <li>✅ IELTS va CEFR tayyorlov darslari</li>
            <li>✅ Matematika, Fizika, Ingliz tili fanlaridan chuqur o‘rganish</li>
            <li>✅ Online va offline darslar</li>
        </ul>
        <p style="font-size: 16px;">Joylar soni cheklangan, shoshiling! 😊</p>
        <div style="text-align: center; margin-top: 30px;">
            <a href="https://o-quvmarkaz-roa0.onrender.com/new/" style="display: inline-block; padding: 12px 24px; background-color: #0d6efd; color: white; text-decoration: none; border-radius: 5px;">
                Kurslarni Ko‘rish
            </a>
        </div>
        <hr style="margin: 30px 0;">
        <p style="font-size: 14px; color: gray; text-align: center;">
            O'quv Markazi &copy; 2025 | <a href="https://t.me/Yoqub_Akhmedov" style="color: gray;">Bog‘lanish (Telegram)</a>
        </p>
    </div>
</body>
</html>
"""


from django.core.mail import EmailMultiAlternatives


def send_html_email(request,):
    subject = "HTML email sinovi"

    from_email =EMAIL_HOST_USER

    to = ["abdullagulomjonov2306@gmail.com"]

    text_content = "Bu oddiy email matni."

    html_content = xabar

    email = EmailMultiAlternatives(subject, text_content, from_email, to)

    email.attach_alternative(html_content, "text/html")

    email.send()

    return HttpResponse(request,'yuborildi')

