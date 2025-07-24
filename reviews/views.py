from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .models import Review
from .forms import ReviewForm

User = get_user_model()

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create.html'
    success_url = reverse_lazy('reviews:list')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            user = self.request.user
            form.instance.author = user
            if not form.cleaned_data.get('author_name'):
                form.instance.author_name = user.get_full_name()
        return super().form_valid(form)

class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/list.html'
    context_object_name = 'reviews'
    queryset = Review.objects.filter(is_published=True).order_by('-created_at')