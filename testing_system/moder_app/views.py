from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from main_app.models import Category, Tag, Test

from .forms import CategoryForm, TagForm


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
        context['categories'] = Category.objects.all().order_by('-created_at')
        return context


@login_required
def test_category_delete(request):
    check_is_moder(request.user)
    cat_slug = request.GET.get('slug_category')
    Category.objects.get(slug=cat_slug).delete()
    return redirect('moder_categories')


class ModerTestTagsView(AccessMixin, CreateView):
    model = Tag
    template_name = 'moder_app/moder_test_tags.html'
    form_class = TagForm
    success_url = reverse_lazy('moder_tags')
    login_url = reverse_lazy('login')
    extra_context = {'cur_section': 'tag'}

    def dispatch(self, request, *args, **kwargs):
        check_is_moder(request.user)
        return super(ModerTestTagsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModerTestTagsView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all().order_by('-created_at')
        return context


@login_required
def test_tag_delete(request):
    check_is_moder(request.user)
    tag_slug = request.GET.get('slug_tag')
    Tag.objects.get(slug=tag_slug).delete()
    return redirect('moder_tags')
