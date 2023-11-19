from django.urls import path

from rating import views

app_name = "rating"

urlpatterns = [
    path(
        "delete/<int:pk>/",
        views.RatingDeleteView.as_view(),
        name="delete_rating",
    ),
    path(
        "update/<int:pk>/",
        views.RatingUpdateView.as_view(),
        name="update_rating",
    ),
]
