from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from .models import Category, Dish

class DishListView(ListView):
    model = Dish
    context_object_name = 'dishes'
    template_name = 'menu/dish_list.html'
    
    def get_queryset(self):
        return Dish.objects.filter(is_active=True).select_related('category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class DishDetailView(DetailView):
    model = Dish
    context_object_name = 'dish'
    template_name = 'menu/dish_detail.html'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Dish.objects.filter(is_active=True).select_related('category')