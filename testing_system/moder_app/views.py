from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from main_app.models import Category, Tag, Test

from .forms import CategoryForm


def check_is_moder(user) -> None:
    if not user.is_moder:
        raise Http404
    return


class ModerPanelView(AccessMixin, TemplateView):
    template_name = 'moder_app/moder_panel.html'
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        check_is_moder(request.user)
        return super(ModerPanelView, self).dispatch(request, *args, **kwargs)


class ModerTestCategoriesView(AccessMixin, CreateView):
    model = Category
    template_name = 'moder_app/moder_test_categories.html'
    form_class = CategoryForm
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('moder_categories')
    extra_context = {'cur_section': 'category'}

    def dispatch(self, request, *args, **kwargs):
        check_is_moder(request.user)
        return super(ModerTestCategoriesView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModerTestCategoriesView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


@login_required
def test_category_delete(request):
    check_is_moder(request.user)
    cat_slug = request.GET.get('slug_category')
    Category.objects.get(slug=cat_slug).delete()
    return redirect('moder_categories')
