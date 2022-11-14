from django.forms import modelformset_factory


class CustomModalFormSetMixin:
    form_count: int = 5
    multiple_formsets: bool = False
    prefix: str = 'form'

    def get_form_count(self):
        if self.form_count <= 0:
            raise ValueError('The value form_count must be positive and cannot be equal to 0')
        return self.form_count

    def get_formset_queryset(self):
        return self.model.objects.none()

    def get_multiple_formset_settings(self):
        return self.request.session['quest_pk']

    def get_formset(self):
        if not self.multiple_formsets:
            return modelformset_factory(self.model, form=self.form_class, extra=self.get_form_count())

        formsets = dict()
        for prefix, form_count in self.get_multiple_formset_settings().items():
            formsets[prefix] = modelformset_factory(self.model, form=self.form_class, extra=form_count)
        return formsets
