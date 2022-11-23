import string

from django.template import Library
from django.urls import reverse

register = Library()


@register.filter(name='digit_to_alpha')
def digit_to_alpha(value: int) -> str:
    return string.ascii_lowercase[value]


@register.filter(name='get_estimate')
def get_estimate(score: int) -> str:
    est_form = '<span class="badge bg-%s">%s</span>'
    estimates = {
        score < 50: est_form % ('danger', 'Unsatisfactory'),
        score < 75: est_form % ('warning', 'Satisfactory'),
        score < 85: est_form % ('primary', 'Good'),
        score >= 85: est_form % ('success', 'Excellent')
    }
    return estimates.get(True)


@register.inclusion_tag('main_app/continue_test_create_modal.html')
def continue_test_create_modal(test_slug, test_title, test_questions):
    context = dict(continue_type=str(), modal_message=str(), test_slug=test_slug, test_title=test_title)
    if not test_questions.exists():
        context['modal_message'] = 'Вы не добавили ни одного вопроса к вашему тесту,' \
                        ' для продолжения укажите сколько вопросов вы хотите добавить.'
        context['continue_type'] = 'question'
        return context
    context['modal_message'] = 'Вы не добавили ответы на вопросы к вашему тесту.'
    context['continue_type'] = 'answer'
    context['quest_pk'] = ', '.join(str(obj.get('pk')) for obj in test_questions.values('pk'))
    return context
