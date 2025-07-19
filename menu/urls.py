from django.urls import path
from .views import DishListView, DishDetailView

app_name = 'menu'

urlpatterns = [
    path('', DishListView.as_view(), name='dish_list'),
    path('<slug:slug>/', DishDetailView.as_view(), name='dish_detail'),
]