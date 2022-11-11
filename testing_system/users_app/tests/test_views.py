from django.contrib.auth.forms import SetPasswordForm
from django.test import TestCase
from django.urls import reverse

from ..views import RegistrationView, LogoutView, PasswordRecoveryView, RecoveryChangePasswordView
from ..models import User
from ..forms import RegistrationForm, LoginForm, PasswordRecoveryForm


class RegistrationViewTestCase(TestCase):
    def test_url(self):
        resp = self.client.get('/users/registration/')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        resp = self.client.get(reverse('registration'))
        self.assertEqual(resp.status_code, 200)

    def test_view_model(self):
        self.assertEqual(RegistrationView.model, User)

    def test_view_template(self):
        resp = self.client.get('/users/registration/')
        self.assertTemplateUsed(resp, 'users_app/register_page.html')

    def test_view_form_class(self):
        form_class = RegistrationView.form_class
        self.assertEqual(form_class, RegistrationForm)

    def test_view_success_url(self):
        success_url = RegistrationView.success_url
        self.assertEqual(success_url, reverse('main'))

    def test_view_login_user_response(self):
        User.objects.create_user(username='TestUser', password='somehardpassword')
        self.client.login(username='TestUser', password='somehardpassword')
        resp = self.client.get('/users/registration/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('main'))

    def test_view_form_valid(self):
        data = {
            'username': 'TestUser1',
            'password1': 'somehardpassword',
            'password2': 'somehardpassword',
        }
        resp = self.client.post('/users/registration/', data=data)
        self.assertEqual(resp.status_code, 302)
        user = User.objects.get(username='TestUser1')
        self.assertTrue(user.is_authenticated)


class LogoutViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='TestUser', password='somehardpassword')

    def setUp(self) -> None:
        self.client.login(username='TestUser', password='somehardpassword')

    def test_url(self):
        resp = self.client.get('/users/logout/')
        self.assertEqual(resp.status_code, 302)

    def test_url_name(self):
        resp = self.client.get(reverse('logout'))
        self.assertEqual(resp.status_code, 302)

    def test_view_redirect_url(self):
        url = LogoutView.url
        self.assertEqual(url, reverse('login'))

    def test_view_non_login_user_response(self):
        self.client.logout()
        resp = self.client.get('/users/logout/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('main'))


class LoginViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='TestUser', password='somehardpassword')

    def test_url(self):
        resp = self.client.get('/users/login/')
        self.assertEqual(resp.status_code, 200)

    def test_url_name(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(reverse('login'))
        self.assertTemplateUsed(resp, 'users_app/login_page.html')

    def test_view_context(self):
        resp = self.client.get(reverse('login'))
        self.assertIn('form', resp.context.keys())

    def test_view_login_user_response(self):
        self.client.login(username='TestUser', password='somehardpassword')
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('main'))

    def test_view_form(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        form = resp.context.get('form')
        self.assertEqual(form.__class__.__name__, LoginForm.__name__)

    def test_view_post_method(self):
        data = dict(username='TestUser', password='somehardpassword')
        resp = self.client.post(reverse('login'), data, follow=True)
        self.assertEqual(resp.status_code, 200)
        user = User.objects.get(username='TestUser')
        self.assertTrue(user.is_authenticated)


class PasswordRecoveryViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='UserPassRec', password='SomeHardPassword')

    def test_view_url(self):
        resp = self.client.get('/users/recovery/word/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_name(self):
        resp = self.client.get(reverse('pass_rec'))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(reverse('pass_rec'))
        self.assertTemplateUsed(resp, 'users_app/recovery/recovery_by_word.html')

    def test_view_form_class(self):
        form_class = PasswordRecoveryView.form_class
        self.assertEqual(form_class.__name__, PasswordRecoveryForm.__name__)

    def test_view_success_url(self):
        success_url = PasswordRecoveryView.success_url
        self.assertEqual(success_url, reverse('pass_change'))

    def test_view_login_user_response(self):
        self.client.login(username='UserPassRec', password='SomeHardPassword')
        resp = self.client.get(reverse('pass_rec'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('main'))

    def test_view_post_method_valid_error(self):
        data = dict(username='UserPassRec', type_secret_word='Hobby', secret_word='SecWor')
        resp = self.client.post(reverse('pass_rec'), data=data, follow=True)
        self.assertEqual(resp.status_code, 200)
        messages = list(resp.context['messages'])
        self.assertEqual(str(messages[0]), 'У данного пользователя не установлено секретное слово')

    def test_view_post_method(self):
        User.objects.filter(username='UserPassRec').update(type_secret_word='Hobby', secret_word='SecWor')
        data = dict(username='UserPassRec', type_secret_word='Hobby', secret_word='SecWor')
        resp = self.client.post(reverse('pass_rec'), data=data, follow=True)
        self.assertEqual(resp.status_code, 200)
        messages = list(resp.context['messages'])
        self.assertEqual(len(messages), 0)
        self.assertEqual(self.client.session['username'], 'UserPassRec')


class RecoveryChangePasswordViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='UserPassChange', password='SomeHardPassword')

    def setUp(self) -> None:
        s = self.client.session
        s.update({'username': 'UserPassChange'})
        s.save()

    def test_view_url(self):
        resp = self.client.get('/users/recovery/change_password/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_name(self):
        resp = self.client.get(reverse('pass_change'))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(reverse('pass_change'))
        self.assertTemplateUsed(resp, 'users_app/recovery/recovery_page.html')

    def test_view_form_class(self):
        form_class = RecoveryChangePasswordView.form_class
        self.assertEqual(form_class.__name__, SetPasswordForm.__name__)

    def test_view_success_url(self):
        success_url = RecoveryChangePasswordView.success_url
        self.assertEqual(success_url, reverse('login'))

    def test_view_dispatch(self):
        session = self.client.session
        session.clear()
        session.save()
        resp = self.client.get(reverse('pass_change'))
        self.assertEqual(resp.status_code, 404)

    def test_view_form_valid(self):
        data = dict(new_password1='NewVeryHardPassword', new_password2='NewVeryHardPassword')
        resp = self.client.post(reverse('pass_change'), data=data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('username', self.client.session.keys())

    def test_view_get_form_kwargs(self):
        user = User.objects.get(username='UserPassChange')
        resp = self.client.get(reverse('pass_change'))
        form = resp.context['form']
        self.assertEqual(user, form.user)
