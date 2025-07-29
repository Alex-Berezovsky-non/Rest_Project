from django.views.generic import ListView
from menu.models import Dish
from .models import GalleryItem
from django.db.models import QuerySet
from typing import Any, Dict, Optional


class DishGalleryView(ListView):
    template_name = 'gallery/dish_gallery.html'
    paginate_by = 12
    context_object_name = 'images'
    dish: Dish  # Аннотация типа для экземпляра переменной

    def get_queryset(self) -> QuerySet[GalleryItem]:
        self.dish = Dish.objects.get(slug=self.kwargs['slug'])
        return self.dish.gallery_items.all()  # type: ignore[attr-defined]

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['dish'] = self.dish
        return context


class FeaturedGalleryView(ListView):
    template_name = 'gallery/featured.html'
    queryset: Optional[QuerySet[GalleryItem]] = GalleryItem.objects.filter(is_featured=True)
    context_object_name = 'images'