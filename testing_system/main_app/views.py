from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .models import Test, TestQuestions, TestAnswers
from .forms import TestForm, TestQuestionsForm, TestAnswersForm
from .utils import CustomModalFormSetMixin


def index(request):
    return render(request, 'base.html')


class TestCreateView(AccessMixin, CreateView):
    model = Test
    template_name = 'main_app/test_create_page.html'
    form_class = TestForm
    success_url = reverse_lazy('quest_create')
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if 'test_slug' in request.session.keys():
            return redirect('quest_create')
        return super(TestCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        author = self.request.user
        self.object.author = author
        if author.is_staff or author.is_moder:
            self.object.is_published = True
        self.object.save()
        self.request.session['test_slug'] = self.object.slug
        self.request.session['quest_count'] = self.request.POST.get('quest_count')
        return super(TestCreateView, self).form_valid(form)


class QuestionsCreateView(AccessMixin, CreateView, CustomModalFormSetMixin):
    model = TestQuestions
    template_name = 'main_app/question_create_page.html'
    form_class = TestQuestionsForm
    login_url = reverse_lazy('login')
    form_count = 3
    prefix = 'question'

    def dispatch(self, request, *args, **kwargs):
        if 'test_slug' not in request.session.keys():
            return redirect('test_create')
        return super(QuestionsCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_count(self):
        return int(self.request.session['quest_count'])

    def get_context_data(self, **kwargs):
        context = super(QuestionsCreateView, self).get_context_data(**kwargs)
        ModalFormSet = self.get_formset()
        context['formset'] = ModalFormSet(queryset=TestQuestions.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        ModalFormSet = self.get_formset()
        formset = ModalFormSet(request.POST, request.FILES)
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            return self.form_invalid(formset)

    def form_valid(self, form):
        instances = form.save(commit=False)
        test_slug = self.request.session['test_slug']
        test_obj = Test.objects.get(slug=test_slug)
        del self.request.session['test_slug']
        del self.request.session['quest_count']
        answers_count = {'Expanded': 1, 'Variable': 4}
        quest_pk = dict()
        for instance in instances:
            instance.test = test_obj
            instance.save()
            quest_pk[instance.pk] = answers_count.get(instance.answers_type)
        self.request.session['quest_pk'] = quest_pk
        return HttpResponseRedirect(reverse('answer_create'))

    def form_invalid(self, form):
        self.render_to_response(self.get_context_data(formset=form))


class AnswersCreateView(AccessMixin, CreateView, CustomModalFormSetMixin):
    model = TestAnswers
    template_name = 'main_app/answer_create_page.html'
    form_class = TestAnswersForm
    login_url = reverse_lazy('login')
    multiple_formsets = True

    def dispatch(self, request, *args, **kwargs):
        if 'quest_pk' not in request.session.keys():
            return redirect('quest_create')
        return super(AnswersCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AnswersCreateView, self).get_context_data(**kwargs)
        formsets_data = self.get_formset()
        formset_queryset = TestAnswers.objects.none()
        questions = TestQuestions.objects.all()
        context['formset_list'] = {
            questions.get(pk=prefix): formset(queryset=formset_queryset, prefix=prefix) for prefix, formset in formsets_data.items()
        }
        return context

    def post(self, request, *args, **kwargs):
        formset_data = {prefix: formset(request.POST, prefix=prefix) for prefix, formset in self.get_formset().items()}
        for formset in formset_data.values():
            if formset.is_valid():
                return self.form_valid(formset_data)
            else:
                return self.form_invalid(formset_data)

    def form_valid(self, formset_list):
        for formset in formset_list.values():
            instances = formset.save(commit=False)
            question = TestQuestions.objects.get(pk=formset.prefix)
            for instance in instances:
                instance.question = question
                instance.save()
        del self.request.session['quest_pk']
        return HttpResponseRedirect(reverse('main'))

    def form_invalid(self, formset_list):
        return self.render_to_response(self.get_context_data(formset_list=formset_list))

