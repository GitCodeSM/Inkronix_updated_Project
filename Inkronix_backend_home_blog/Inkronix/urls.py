
from django.contrib import admin
from django.urls import path, include
from Inkronix import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import blog.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/',include(blog.urls)),
    path('course',include('course.urls')),
    path('account', include("accounts.urls")),
    path('', include("inkronixapp.urls"))
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
