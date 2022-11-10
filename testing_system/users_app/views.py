from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.views.generic import RedirectView
from django.contrib.auth.forms import SetPasswordForm

from .models import User
from .forms import RegistrationForm, LoginForm, PasswordRecoveryForm


class RegistrationView(CreateView):
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
    url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('main')
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


def login_view(request):
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
