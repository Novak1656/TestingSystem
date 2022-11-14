from django.forms import modelformset_factory
from .models import TestQuestions


class CustomModalFormSetMixin:
    """
    Миксин для упрощения создания как одиночных так и наборов формсетов
    """
    form_count: int = 5
    multiple_formsets: bool = False
    prefix: str = 'form'
    multiple_formset_setting_kwarg: dict = None

    def get_form_count(self):
        if self.form_count <= 0:
            raise ValueError('The value form_count must be positive and cannot be equal to 0')
        return self.form_count

    def get_formset_queryset(self):
        return self.model.objects.none()

    def get_multiple_formset_settings(self):
        if not self.multiple_formset_setting_kwarg:
            raise ValueError('Value multiple_formset_setting_kwarg is not exists')
        return self.request.session[self.multiple_formset_setting_kwarg]

    def get_formset(self):
        if not self.multiple_formsets:
            return modelformset_factory(self.model, form=self.form_class, extra=self.get_form_count())

        formsets = dict()
        formset_settings = self.get_multiple_formset_settings()
        queryset_dict = {obj.pk: obj for obj in TestQuestions.objects.filter(pk__in=formset_settings.keys())}
        for prefix, form_count in formset_settings.items():
            instance = queryset_dict.get(int(prefix))
            if instance.answers_type == 'Expanded':
                formsets[instance] = modelformset_factory(self.model, form=self.form_class,
                                                          extra=form_count, exclude=['is_right'])
                continue
            formsets[instance] = modelformset_factory(self.model, form=self.form_class, extra=form_count)
        return formsets
