from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import (RegistrationView, LogoutView, login_view, PasswordRecoveryView, RecoveryChangePasswordView,
                    UserProfileView, UserResultsListView, UserTestsListView, UserTestDelete, UserTestAnswersListView,
                    UserSettings, change_user_names, change_user_username, change_user_email, change_user_password,
                    change_user_secret_word)


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

    path('profile/', login_required(UserProfileView.as_view()), name='profile'),
    path('profile/my_results/', login_required(UserResultsListView.as_view()), name='my_results'),
    path('profile/my_tests/', login_required(UserTestsListView.as_view()), name='my_tests'),
    path('profile/my_tests/delete_test/', login_required(UserTestDelete.as_view()), name='test_delete'),
    path('profile/my_tests/answers/<str:test_slug>/',
         login_required(UserTestAnswersListView.as_view()),
         name='test_answers'),

    path('profile/settings/', login_required(UserSettings.as_view()), name='user_settings'),
    path('profile/settings/change_names/', change_user_names, name='change_user_names'),
    path('profile/settings/change_username/', change_user_username, name='change_user_username'),
    path('profile/settings/change_email/', change_user_email, name='change_user_email'),
    path('profile/settings/change_password/', change_user_password, name='change_user_password'),
    path('profile/settings/change_user_secret_word/', change_user_secret_word, name='change_user_secret_word'),
]
