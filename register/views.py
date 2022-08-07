from django.views.generic import FormView

from .forms import RegisterForm


class RegisterFormView(FormView):
    """Simple user registration view"""

    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)
