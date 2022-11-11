from django.test import TestCase
from ..forms import RegistrationForm, LoginForm, PasswordRecoveryForm
from ..models import User
from django.forms import TextInput, Select


class RegistrationFormTestCase(TestCase):
    def setUp(self) -> None:
        self.form_meta = RegistrationForm._meta
        self.data = {
            'username': 'TestUser',
            'password1': 'somehardpassword',
            'password2': 'somehardpassword',
            'type_secret_word': 'Hobby',
            'secret_word': 'superhardword',
        }

    def test_form_model(self):
        form_model = self.form_meta.model
        self.assertEqual(form_model, User)

    def test_form_fields(self):
        form_fields = self.form_meta.fields
        fields_list = ['username', 'first_name', 'last_name', 'email', 'type_secret_word',
                       'secret_word', 'password1', 'password2']
        self.assertEqual(form_fields, fields_list)

    def test_form_fields_widgets_attrs(self):
        form = RegistrationForm()
        form_fields = ['username', 'first_name', 'last_name', 'email', 'type_secret_word', 'secret_word']
        for field in form_fields:
            self.assertEqual(form.fields[field].widget.attrs['class'], 'form-control')

    def test_clean_secret_word_field(self):
        self.data.pop('secret_word')
        form = RegistrationForm(self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['secret_word'][0], 'Введите секретное слово')

    def test_clean_type_secret_word_field(self):
        self.data.pop('type_secret_word')
        form = RegistrationForm(self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['secret_word'][0], 'Выберите тип секретного слова')


class LoginFormTestCase(TestCase):
    def setUp(self) -> None:
        self.form = LoginForm()

    def test_username_field(self):
        field = self.form.fields['username']
        self.assertEqual(field.label, 'Логин')
        self.assertEqual(field.widget.attrs['class'], 'form-control')

    def test_password_field(self):
        field = self.form.fields['password']
        self.assertEqual(field.label, 'Пароль')
        self.assertEqual(field.widget.attrs['class'], 'form-control')

    def test_remember_me_field(self):
        field = self.form.fields['remember_me']
        self.assertEqual(field.label, 'Запомнить меня')


class PasswordRecoveryFormTestCase(TestCase):
    def setUp(self) -> None:
        self.fields = PasswordRecoveryForm().fields

    def test_username_field(self):
        field = self.fields['username']
        self.assertEqual(field.label, 'Логин')
        self.assertEqual(field.help_text, 'Введите ваш логин')
        self.assertEqual(field.widget.__class__.__name__, TextInput.__name__)
        self.assertEqual(field.widget.attrs['class'], 'form-control')

    def test_type_secret_word_field(self):
        field = self.fields['type_secret_word']
        self.assertEqual(field.label, 'Категория секретного слова')
        self.assertEqual(field.help_text, 'Выберите категорию к которой относится ваше секретное слово')
        self.assertEqual(field.widget.__class__.__name__, Select.__name__)
        self.assertEqual(field.widget.attrs['class'], 'form-control')
        choices_list = User.SECRET_WORD_TYPES
        self.assertEqual(field.widget.choices, choices_list)

    def test_secret_word_field(self):
        field = self.fields['secret_word']
        self.assertEqual(field.label, 'Секретное слово')
        self.assertEqual(field.help_text, 'Введите ваше секретное слово')
        self.assertEqual(field.widget.__class__.__name__, TextInput.__name__)
        self.assertEqual(field.widget.attrs['class'], 'form-control')

    def test_clean_username(self):
        data = dict(username='NotExistingUser', type_secret_word='Hobby', secret_word='SomeSecretWord')
        form = PasswordRecoveryForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'][0], 'Пользователь "NotExistingUser" не существует')
