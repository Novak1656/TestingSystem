from django import forms
from .models import Test, Tag, TestQuestions, TestAnswers


class TestForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        label='Теги',
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Test
        fields = ['title', 'description', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }


class TestQuestionsForm(forms.ModelForm):
    class Meta:
        model = TestQuestions
        fields = ['question', 'image', 'answers_type']
        widgets = {
            'question': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 50px;'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'answers_type': forms.Select(attrs={'class': 'form-control'})
        }


class TestAnswersForm(forms.ModelForm):
    class Meta:
        model = TestAnswers
        fields = ['answer', 'is_right']
        widgets = {
            'answer': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 20px;'}),
            'is_right': forms.CheckboxInput()
        }
