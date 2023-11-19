from django.urls import path

from rating import views

app_name = "rating"
urlpatterns = [
    path("<int:pk>/", views.RatingDelete.as_view(), name="delete_rating"),
]
