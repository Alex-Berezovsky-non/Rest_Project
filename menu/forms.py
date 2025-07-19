from django import forms
from .models import Dish

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'category', 'ingredients', 'price', 'image']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Цена должна быть положительной")
        return price