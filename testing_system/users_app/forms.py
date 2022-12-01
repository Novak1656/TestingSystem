from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from .models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'type_secret_word',
                  'secret_word', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'type_secret_word': forms.Select(attrs={'class': 'form-control'}),
            'secret_word': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_secret_word(self):
        word = self.cleaned_data['secret_word']
        word_type = self.cleaned_data['type_secret_word']
        if not word and word_type:
            raise ValidationError('Введите секретное слово')
        elif word and not word_type:
            raise ValidationError('Выберите тип секретного слова')
        return word


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    remember_me = forms.BooleanField(label='Запомнить меня', widget=forms.CheckboxInput(), required=False)


class PasswordRecoveryForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        help_text='Введите ваш логин',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    type_secret_word = forms.CharField(
        label='Категория секретного слова',
        help_text='Выберите категорию к которой относится ваше секретное слово',
        widget=forms.Select(choices=User.SECRET_WORD_TYPES, attrs={'class': 'form-control'})
    )
    secret_word = forms.CharField(
        label='Секретное слово',
        help_text='Введите ваше секретное слово',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if not user.exists():
            raise ValidationError(f'Пользователь "{username}" не существует')
        return username


class UserNamesForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}


class UserEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {'email': forms.EmailInput(attrs={'class': 'form-control'})}


class UserPasswordForm(forms.Form):
    password1 = forms.CharField(
        label='Пароль',
        help_text='Введите новый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        help_text='Введите пароль ещё раз',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def clean_password1(self):
        password = self.cleaned_data['password1']
        if len(password) < 8:
            raise ValidationError('Длинна пароля должна составлять минимум 8 символов')
        return password


class UserSecretWordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['type_secret_word', 'secret_word']
        widgets = {
            'type_secret_word': forms.Select(attrs={'class': 'form-control'}),
            'secret_word': forms.TextInput(attrs={'class': 'form-control'})
        }
