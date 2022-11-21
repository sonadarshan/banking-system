from django.views.generic import TemplateView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy

class HomeView(TemplateView):
    template_name = 'core/landing.html'
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:profile')
            )
        return super().dispatch(request, *args, **kwargs)
