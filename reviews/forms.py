from typing import Any
from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.HiddenInput(),
        error_messages={
            'required': 'Пожалуйста, выберите оценку'
        }
    )

    class Meta:
        model = Review
        fields = ['author_name', 'rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4})
        }
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.author:
            self.fields['author_name'].initial = self.instance.author.get_full_name()