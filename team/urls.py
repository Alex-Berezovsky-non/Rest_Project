from django.urls import path
from .views import TeamListView

app_name = 'team'

urlpatterns = [
    path('', TeamListView.as_view(), name='team_list'),
]