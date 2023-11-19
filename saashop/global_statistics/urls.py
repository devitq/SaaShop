from django.urls import path

from global_statistics import views


app_name = "global_statistics"
urlpatterns = [
    path(
        "all_items/",
        views.all_items,
        name="all_items",
    ),
    path(
        "user_items/",
        views.user_items,
        name="user_items",
    ),
    path(
        "all_users/",
        views.all_users,
        name="all_users",
    ),
]
