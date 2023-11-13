from django.contrib.auth import views
from django.urls import path

import users.views

app_name = "users"

urlpatterns = [
    path("signup/", users.views.UserSignupView.as_view(), name="signup"),
    path("users/", users.views.UserListView.as_view(), name="user_list"),
    path(
        "user/<int:pk>/",
        users.views.UserDetailView.as_view(),
        name="user_detail",
    ),
    path("profile/", users.views.profile_edit, name="profile"),
    path(
        "login/",
        views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path(
        "activate/<str:uidb64>/<str:token>/",
        users.views.ActivateAccountView.as_view(),
        name="activate_account",
    ),
]
