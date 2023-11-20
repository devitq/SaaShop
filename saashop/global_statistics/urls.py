from django.urls import path

from global_statistics import views


app_name = "global_statistics"
urlpatterns = [
    path(
        "all_items/",
        views.AllItemsView.as_view(),
        name="all_items",
    ),
    path(
        "user_items/",
        views.UserItemsView.as_view(),
        name="user_items",
    ),
    path(
        "all_users/",
        views.AllUsersView.as_view(),
        name="all_users",
    ),
]
