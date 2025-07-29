from django.urls import path
from .views import DishGalleryView, FeaturedGalleryView

app_name = 'gallery'

urlpatterns = [
    path('dishes/<slug:slug>/', DishGalleryView.as_view(), name='dish_gallery'),
    path('featured/', FeaturedGalleryView.as_view(), name='featured'),
]