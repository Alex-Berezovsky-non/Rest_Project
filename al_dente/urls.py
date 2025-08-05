from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from reservations.views import HallMapView 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),          # Главная страница
    path('menu/', include('menu.urls')),     # Меню
    path('gallery/', include('gallery.urls')),  # Галерея
    path('team/', include('team.urls')),     # Команда 
    path('api/reservations/', include('reservations.urls')),  # API бронирования
    path('reviews/', include('reviews.urls')),  # Отзывы
    path('events/', include('events.urls')), # События
    path('api/reservations/', include('reservations.urls')),  # API бронирования
    path('map/', HallMapView.as_view(), name='map'),  # Карта зала
]

# Обработка медиа-файлов ТОЛЬКО в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)