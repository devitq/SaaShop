from django.urls import path

from . import views

app_name = "download"
urlpatterns = [path("<path:path>", views.download, name="download")]
