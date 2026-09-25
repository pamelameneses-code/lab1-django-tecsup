from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['exam', 'text', 'score']
        widgets = {
            'exam': forms.Select(attrs={'class': 'form-select'}),
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enunciado de la pregunta'}),
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BaseChoiceFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        
        correct_count = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct'):
                    correct_count += 1
        
        if correct_count != 1:
            raise ValidationError("Debes marcar exactamente una opción como correcta.")

ChoiceFormSet = inlineformset_factory(
    Question,
    Choice,
    fields=['text', 'is_correct'],
    extra=4,
    max_num=4,
    can_delete=False,
    formset=BaseChoiceFormSet,
    widgets={
        'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto de la opción'}),
        'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }
)