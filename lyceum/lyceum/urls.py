from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("about/", include("about.urls")),
    path("catalog/", include("catalog.urls")),
    path("download/", include("download.urls")),
    path("feedback/", include("feedback.urls")),
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
]

if settings.MEDIA_ROOT and settings.USE_LOCAL_MEDIA:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
