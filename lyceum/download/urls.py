from django.urls import path

from download import views

app_name = "download"
urlpatterns = [path("<path:path>", views.download, name="download")]
