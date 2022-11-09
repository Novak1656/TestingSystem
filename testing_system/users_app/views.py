from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import RedirectView

from .models import User
from .forms import RegistrationForm, LoginForm


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
