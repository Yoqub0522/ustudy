from django.apps import AppConfig



class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
    def ready(self):
        from user.Signal import send_gmail_user,reset_password,send_gmail_html




