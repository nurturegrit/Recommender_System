from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .forms import CompleteProfileForm

class CompleteProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CompleteProfileForm
    template_name = 'users/complete_profile.html'
    success_url = '/'  # Redirect to home after completion
    
    def get_object(self, queryset=None):
        return self.request.user