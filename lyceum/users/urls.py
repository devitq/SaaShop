from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("signup/", views.UserSignupView.as_view(), name="signup"),
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("user/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("profile/", views.profile_edit, name="profile"),
    path(
        "login/",
        views.MyLoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        views.MyLogoutView.as_view(),
        name="logout",
    ),
    path(
        "password-change/",
        views.MyPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change/done/",
        views.MyPasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "password-reset/",
        views.MyPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        views.MyPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset/confirm/<str:uidb64>/<str:token>/",
        views.MyPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        views.MyPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "activate/<str:uidb64>/<str:token>/",
        views.ActivateAccountView.as_view(),
        name="activate_account",
    ),
]
