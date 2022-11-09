from django.urls import path
from .views import RegistrationView, LogoutView, login_view


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', login_view, name='login'),
]
