from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView
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


class QuestionsCreateView(AccessMixin, FormView, CustomModalFormSetMixin):
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
        if 'formset' not in context.keys():
            ModalFormSet = self.get_formset()
            context['formset'] = ModalFormSet(queryset=TestQuestions.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        ModalFormSet = self.get_formset()
        formset = ModalFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data == {}:
                    messages.error(request, 'Fill in all the fields for questions')
                    return self.render_to_response(self.get_context_data(formset=formset))
                # Сделать валидатор для формсета
            #return self.form_valid(formset)
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


class AnswersCreateView(AccessMixin, FormView, CustomModalFormSetMixin):
    model = TestAnswers
    template_name = 'main_app/answer_create_page.html'
    form_class = TestAnswersForm
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('main')
    multiple_formsets = True
    multiple_formset_setting_kwarg = 'quest_pk'

    def dispatch(self, request, *args, **kwargs):
        if 'quest_pk' not in request.session.keys():
            return redirect('quest_create')
        return super(AnswersCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AnswersCreateView, self).get_context_data(**kwargs)
        formsets_data = self.get_formset()
        formset_queryset = TestAnswers.objects.none()
        if 'formset_list' not in context.keys():
            context['formset_list'] = {
                quest: formset(queryset=formset_queryset, prefix=quest.pk) for quest, formset in formsets_data.items()
            }
        return context

    def post(self, request, *args, **kwargs):
        formset_data = {quest: formset(request.POST, prefix=quest.pk) for quest, formset in self.get_formset().items()}
        for question, formset in formset_data.items():
            if formset.is_valid():
                right_answers = [form.cleaned_data['is_right'] for form in formset if 'is_right' in form.cleaned_data.keys()]
                if right_answers.count(True) == 0:
                    messages.error(request, 'Select one or more right answers')
                    return self.render_to_response(self.get_context_data(formset_list=formset_data))
                return self.form_valid(formset_data)
            else:
                return self.form_invalid(formset_list=formset_data)

    def form_valid(self, formset_list):
        for question, formset in formset_list.items():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.question = question
                instance.save()
        del self.request.session['quest_pk']
        return HttpResponseRedirect(reverse('main'))

    def form_invalid(self, formset_list):
        return self.render_to_response(self.get_context_data(formset_list=formset_list))

