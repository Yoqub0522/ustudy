from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

# from asosiy.settings import MEDIA_URL

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('new/', include('new.urls')),
    path('elon/', include('elon.urls')),
    path('', include('user.urls')),
    path('captcha/', include('captcha.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns +=[
        re_path(r''
                r'^rosetta/',include('rosetta.urls')),
    ]