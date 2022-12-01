from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, FormView, TemplateView, ListView
from django.views.generic import RedirectView
from django.contrib.auth.forms import SetPasswordForm

from .models import User
from .forms import (RegistrationForm, LoginForm, PasswordRecoveryForm, UserNamesForm, UserUsernameForm, UserEmailForm,
                    UserPasswordForm, UserSecretWordForm)


class RegistrationView(CreateView):
    """
        Представление для рагистрации пользователя
    """
    model = User
    template_name = 'users_app/register_page.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('main')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main')
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        login(self.request, self.object)
        return super(RegistrationView, self).form_valid(form)


class LogoutView(RedirectView):
    """
        Представление выхода из аккаунта пользователя
    """
    url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('main')
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


def login_view(request):
    """
        Представление для авторизации пользователя
    """
    if request.user.is_authenticated:
        return redirect('main')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            remember_me = form.cleaned_data['remember_me']
            if not remember_me:
                request.session.set_expiry(0)
                request.session.modified = True
            login(request, user)
            return redirect('main')
    else:
        form = LoginForm()
    return render(request, 'users_app/login_page.html', {'form': form})


class PasswordRecoveryView(FormView):
    """
        Представление для восстановления пароля пользователя
    """
    template_name = 'users_app/recovery/recovery_by_word.html'
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy('pass_change')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main')
        return super(PasswordRecoveryView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data['username']
            secret_word = form.cleaned_data['secret_word']
            user = User.objects.filter(Q(username=username) & Q(secret_word=secret_word))
            if not user.exists():
                messages.error(request, 'У данного пользователя не установлено секретное слово')
                return self.render_to_response(self.get_context_data(form=form))
            request.session['username'] = username
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class RecoveryChangePasswordView(FormView):
    """
        Представление установки нового пароля пользователя
    """
    template_name = 'users_app/recovery/recovery_page.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if 'username' not in request.session.keys():
            raise Http404
        return super(RecoveryChangePasswordView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.session.clear()
        form.save()
        return super(RecoveryChangePasswordView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = {
            'user': User.objects.get(username=self.request.session['username']),
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs


class UserProfileView(AccessMixin, TemplateView):
    """
        Представление для профиля пользователя
    """
    template_name = 'users_app/user_profile/profile.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context.update({'user': self.request.user})
        return context


class UserResultsListView(AccessMixin, ListView):
    """
        Представление для результатов тестирования пользователя
    """
    template_name = 'users_app/user_profile/user_results.html'
    context_object_name = 'results'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        user = self.request.user
        return user.results.all().prefetch_related('right_answers', 'test__questions').select_related('test')


class UserTestsListView(AccessMixin, ListView):
    """
        Представление для тестов пользователя
    """
    template_name = 'users_app/user_profile/user_tests.html'
    context_object_name = 'tests'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        user = self.request.user
        return user.tests.all().prefetch_related('questions', 'questions__answers', 'tags').select_related('category')


class UserTestDelete(AccessMixin, RedirectView):
    """
        Представление для удаление теста пользователя
    """
    url = reverse_lazy('my_tests')
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        request.user.tests.get(slug=request.GET.get('test_slug')).delete()
        return super(UserTestDelete, self).get(request, *args, **kwargs)


class UserTestAnswersListView(AccessMixin, ListView):
    """
        Представление для ответов на вопрос текста пользователя
    """
    template_name = 'users_app/user_profile/user_test_answers.html'
    context_object_name = 'questions'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        user = self.request.user
        test_slug = self.kwargs.get('test_slug')
        return user.tests.get(slug=test_slug).questions.all().prefetch_related('answers')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserTestAnswersListView, self).get_context_data(**kwargs)
        user = self.request.user
        test_slug = self.kwargs.get('test_slug')
        context['test_title'] = user.tests.filter(slug=test_slug).values_list('title', flat=True).first()
        return context


def update_context(user_instance, context: dict) -> dict:
    """
        Функция для обновления контекста страницы настроек пользователя
    """
    if not context.get('names_form'):
        context['names_form'] = UserNamesForm(instance=user_instance)
    if not context.get('username_form'):
        context['username_form'] = UserUsernameForm(instance=user_instance)
    if not context.get('email_form'):
        context['email_form'] = UserEmailForm(instance=user_instance)
    if not context.get('password_form'):
        context['password_form'] = UserPasswordForm()
    if not context.get('secret_word_form'):
        context['secret_word_form'] = UserSecretWordForm(instance=user_instance)
    return context


class UserSettings(AccessMixin, TemplateView):
    template_name = 'users_app/user_profile/user_settings.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(UserSettings, self).get_context_data(**kwargs)
        return update_context(user_instance=self.request.user, context=context)


@login_required
@require_http_methods(['POST'])
def change_user_names(request):
    """
        Представление для смены фамилии и имени пользователя
    """
    user = request.user
    form = UserNamesForm(request.POST, instance=user)
    change_message = None
    if form.is_valid():
        form.save()
        change_message = '<h3 class="display-6 bg-success text-dark rounded">Вы успешно сменили имя/фамилию</h3>'
    context = dict(
        names_form=form,
        success_message=change_message
    )
    new_context = update_context(user_instance=user, context=context)
    return TemplateResponse(request=request, template='users_app/user_profile/user_settings.html', context=new_context)


@login_required
def change_user_username(request):
    """
        Представление для смены username пользователя
    """
    user = request.user
    form = UserUsernameForm(request.POST, instance=user)
    change_message = '<h3 class="display-6 bg-danger text-dark rounded">Логин не был изменён</h3>'
    if form.is_valid():
        form.save()
        change_message = '<h3 class="display-6 bg-success text-dark rounded">Вы успешно сменили логин</h3>'
    context = dict(
        username_form=form,
        change_message=change_message
    )
    new_context = update_context(user_instance=user, context=context)
    return TemplateResponse(request=request, template='users_app/user_profile/user_settings.html', context=new_context)


@login_required
def change_user_email(request):
    """
        Представление для смены email пользователя
    """
    user = request.user
    form = UserEmailForm(request.POST, instance=user)
    change_message = '<h3 class="display-6 bg-danger text-dark rounded">Email не был изменён</h3>'
    if form.is_valid():
        form.save()
        change_message = '<h3 class="display-6 bg-success text-dark rounded">Вы успешно сменили email</h3>'
    context = dict(
        email_form=form,
        change_message=change_message
    )
    new_context = update_context(user_instance=user, context=context)
    return TemplateResponse(request, 'users_app/user_profile/user_settings.html', new_context)


@login_required
def change_user_password(request):
    """
        Представление для смены пароля пользователя
    """
    user = request.user
    form = UserPasswordForm(request.POST)
    change_message = '<h3 class="display-6 bg-danger text-dark rounded">Пароль не был изменён</h3>'
    if form.is_valid():
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        if password1 != password2:
            change_message = '<h3 class="display-6 bg-danger text-dark rounded">Пароли не совпадают</h3>'
        else:
            user.set_password(password1)
            user.save()
            change_message = '<h3 class="display-6 bg-success text-dark rounded">Вы успешно сменили пароль</h3>'
    context = dict(
        password_form=form,
        change_message=change_message
    )
    new_context = update_context(user_instance=user, context=context)
    return TemplateResponse(request, 'users_app/user_profile/user_settings.html', new_context)


@login_required
def change_user_secret_word(request):
    """
        Представление для смены секретного слова пользователя
    """
    user = request.user
    form = UserSecretWordForm(request.POST, instance=user)
    change_message = '<h3 class="display-6 bg-danger text-dark rounded">Секретное слово не было изменёно</h3>'
    if form.is_valid():
        form.save()
        change_message = '<h3 class="display-6 bg-success text-dark rounded">Вы успешно сменили секретное слово</h3>'
    context = dict(
        secret_word_form=form,
        change_message=change_message
    )
    new_context = update_context(user_instance=user, context=context)
    return TemplateResponse(request, 'users_app/user_profile/user_settings.html', new_context)
