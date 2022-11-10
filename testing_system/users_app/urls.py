from django.contrib.auth import views
from django.urls import path
from .views import RegistrationView, LogoutView, login_view, PasswordRecoveryView, RecoveryChangePasswordView


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', login_view, name='login'),

    path('recovery/word/', PasswordRecoveryView.as_view(), name='pass_rec'),
    path('recovery/change_password/', RecoveryChangePasswordView.as_view(), name='pass_change'),

    path(
        'password-reset/',
        views.PasswordResetView.as_view(template_name='users_app/recovery/password_reset_form.html'),
        name='password_reset'
         ),
    path(
        'password-reset/done/',
        views.PasswordResetDoneView.as_view(template_name='users_app/recovery/password_reset_complete.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(template_name='users_app/recovery/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        views.PasswordResetCompleteView.as_view(template_name='users_app/recovery/password_reset_done.html'),
        name='password_reset_complete'
    ),
]
