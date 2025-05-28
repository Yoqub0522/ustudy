from  django.urls import path
from django.contrib.auth import views as auth_views

from user.views import register, logout_view, user_stats_page, contact_admin, send_reset_code_view, reset_password_view, \
    google_login, google_callback

from django.urls import path

from .utils import send_message, send_html_email
from .views import UserStatsView



urlpatterns = [
    path('register/', register, name='register'),
    path('',auth_views.LoginView.as_view(template_name='login.html') , name='login'),

    path('logout/', logout_view, name='logout'),

    path('api/user-stats/', UserStatsView.as_view(), name='user-stats'),
    path('stats/', user_stats_page, name='user-stats-page'),
    path('send/', send_message, name='senda'),
    path('mail/', send_html_email, name='send'),
    path('support/',contact_admin, name='support'),
    #parol
    path('send-reset-code/', send_reset_code_view, name='send_reset_code'),
    path('reset-password/<uuid:token>/', reset_password_view, name='reset_password'),
    path('google/', google_login, name='google-login'),
    path('google/login/callback/',google_callback, name='googlepage'),
]


