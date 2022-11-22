import string
from django.template import Library

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
