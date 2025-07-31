from django.views.generic import ListView
from .models import TeamMember

class TeamListView(ListView):
    model = TeamMember
    template_name = 'team/team_list.html'
    context_object_name = 'members'

    def get_queryset(self):
        return TeamMember.objects.filter(is_visible=True).order_by('order')