from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    # LOGIN / LOGOUT
    path("login/", LoginView.as_view(
        template_name="accounts/login.html",
        authentication_form=LoginForm,
        redirect_authenticated_user=True
    ), name="login"),

    path("logout/", LogoutView.as_view(), name="logout"),

    # PASSWORD CHANGE (usuario logueado)
    path("password/change/", auth_views.PasswordChangeView.as_view(
        template_name="accounts/password_change_form.html",
        success_url="/accounts/password/change/done/"
    ), name="password_change"),

    path("password/change/done/", auth_views.PasswordChangeDoneView.as_view(
        template_name="accounts/password_change_done.html"
    ), name="password_change_done"),

    # PASSWORD RESET (flujo por correo)
    path("password/reset/", auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset_form.html",
        email_template_name="accounts/email/password_reset_email.txt",
        subject_template_name="accounts/email/password_reset_subject.txt",
        success_url="/accounts/password/reset/done/"
    ), name="password_reset"),

    path("password/reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"
    ), name="password_reset_done"),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html",
        success_url="/accounts/reset/complete/"
    ), name="password_reset_confirm"),

    path("reset/complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"
    ), name="password_reset_complete"),
]
