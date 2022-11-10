from django.test import TestCase
from django.urls import reverse

from ..views import RegistrationView, LogoutView
from ..models import User
from ..forms import RegistrationForm, LoginForm


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
