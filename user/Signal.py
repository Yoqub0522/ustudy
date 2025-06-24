from django.db import models

from user.models import CustomUser, Profile
from user.utils import send_html_email,xabar
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from asosiy.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives

@receiver(post_save,sender=CustomUser)
def send_gmail_user(sender,instance,created,**kwargs):
    if created:


        send_mail(
                subject="Yangi foydalanuvchi",
                message=f"salom {instance.username} siz ro'yxatdan muvofaqqiyatli o'tdingiz",
                from_email=EMAIL_HOST_USER,
                recipient_list=[instance.email,EMAIL_HOST_USER],
                fail_silently=False,
            )

@receiver(post_save, sender=CustomUser)
def send_gmail_html(sender, instance, created, **kwargs):
    if created:
        subject = "Kurslarga taklif"
        from_email = EMAIL_HOST_USER
        to = [instance.email]
        text_content = f"Salom {instance.username}, siz kurslar platformasiga muvaffaqiyatli qo‘shildingiz."

        email = EmailMultiAlternatives(subject,text_content, from_email, to)
        email.attach_alternative(xabar, "text/html")
        email.send()







from django.contrib.auth import get_user_model
User = get_user_model()
@receiver(pre_save, sender=User)
def reset_password(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_user = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return

    if old_user.password != instance.password:
        send_mail(
            subject='Parolingiz o‘zgartirildi',
            message=(
                f"Salom {instance.username},\n\n"
                f"Sizning parolingiz muvaffaqiyatli o‘zgartirildi.\n"
                f"Agar bu amalni siz bajarmagan bo‘lsangiz, darhol ma'muriyatga murojaat qiling."
            ),
            from_email=EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False
        )



@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()