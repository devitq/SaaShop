from django.urls import path

from global_statistics import views


app_name = "global_statistics"

urlpatterns = [
    path(
        "items/",
        views.AllItemsView.as_view(),
        name="all_items",
    ),
    path(
        "items/my",
        views.UserItemsView.as_view(),
        name="user_items",
    ),
    path(
        "users/",
        views.AllUsersView.as_view(),
        name="all_users",
    ),
]
