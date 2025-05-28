from datetime import datetime, time
import logging

from django.http import HttpResponse



class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        now = datetime.now().time()
        ip = request.META.get('HTTP_USER_AGENT','Nomalum ip')
        print(f'user-agent: {ip}')
        # start_time = time(0, 1, 0)
        # end_time = time(23, 0, 0)
        # if not (start_time <= now <= end_time):
        #     return HttpResponse("<h1>Saytdan faqat 09:00 dan 18:00 gacha foydalanish mumkin!</h1>", status=403)

        response = self.get_response(request)
        return response
import time
from collections import defaultdict
from django.http import HttpResponse

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # IP manzillar bo‘yicha so‘rov vaqtlari
        self.ip_requests = defaultdict(list)
        # Cheklov parametrlarini sozlang
        self.time_window = 10
        self.max_requests = 10

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        now = time.time()

        # Eski vaqtlardan tozalash
        request_times = self.ip_requests[ip]
        request_times = [t for t in request_times if now - t < self.time_window]
        request_times.append(now)
        self.ip_requests[ip] = request_times

        if len(request_times) > self.max_requests:
            return HttpResponse(
                "<h1>Ko‘p so‘rov yubordingiz. Iltimos, 10 soniyadan keyin qayta urinib ko‘ring.</h1>",
                status=429
            )

        response = self.get_response(request)
        return response

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from user_agents import parse
import logging

logger = logging.getLogger('telegram')






def get_client_info(request):
    # IP manzilini aniqlash
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', 'unknown')

    # User-Agent orqali qurilma, OS va brauzerni aniqlash
    ua_string = request.META.get('HTTP_USER_AGENT', 'unknown')
    user_agent = parse(ua_string)

    device = user_agent.device.family or "Unknown Device"
    os = f"{user_agent.os.family} {user_agent.os.version_string}" or "Unknown OS"
    browser = f"{user_agent.browser.family} {user_agent.browser.version_string}" or "Unknown Browser"

    return ip, device, os, browser

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip, device, os, browser = get_client_info(request)
    logger.info(
        f"User saytga kirdi: {user.username} (ID: {user.id}), IP: {ip}, "
        f"Qurilma: {device}, OS: {os}, Brauzer: {browser}"

    )
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from crum import get_current_user
import logging
from new.models import Course, Student

logger = logging.getLogger('telegram')

@receiver(post_save, sender=Course)
def log_course_created(sender, instance, created, **kwargs):
    if created:
        user = get_current_user()
        creator = user.username if user and user.is_authenticated else 'Noma\'lum foydalanuvchi'
        logger.info(f"Yangi Course yaratildi: {instance.name}, Yaratuvchi: {creator}")

    else:
        user = get_current_user()
        creator = user.username if user and user.is_authenticated else 'Noma\'lum foydalanuvchi'
        logger.info(f"Kurs yangilandi: {instance.name}, Editor: {creator}")

@receiver(post_delete, sender=Course)
def log_course_delete(sender, instance, **kwargs):
    user = get_current_user()
    creator = user.username if user and user.is_authenticated else 'Noma\'lum foydalanuvchi'
    logger.info(f"Course o'chirildi: {instance.name}, o'chirgan: {creator}")

@receiver(post_save, sender=Student)
def log_student_created(sender, instance, created, **kwargs):
    if created:
        user = get_current_user()
        creator = user.username if user and user.is_authenticated else 'Noma\'lum foydalanuvchi'
        logger.info(f"Yangi Student yaratildi: {instance.full_name}, Yaratuvchi: {creator}")

    else:
        user = get_current_user()
        creator = user.username if user and user.is_authenticated else 'Noma\'lum foydalanuvchi'
        logger.info(f"Talaba yangilandi: {instance.name}, Editor: {creator}")


@receiver(post_delete, sender=Student)
def log_course_delete(sender, instance, **kwargs):
    user = get_current_user()
    creator = user.username if user and user.is_authenticated else 'Noma\'lum foydalanuvchi'
    logger.warning(f"Student yangilandi: {instance.name}, o'chirgan: {creator}")