from django.template import Library

register = Library()


@register.inclusion_tag('moder_app/moder_section_panel.html')
def get_section_panel(cur_section):
    return {'cur_section': cur_section}


@register.filter(name='tags_list')
def tags_list(tags_queryset):
    tag_list = tags_queryset.values_list('title', flat=True)
    return ', '.join(tag_list)
