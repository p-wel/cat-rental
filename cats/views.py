"""
Views used in cat app
"""

import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView, FormMixin
from django.views.generic.list import MultipleObjectMixin

from cats.forms import RentalForm, SearchForm
from cats.models import Cat, Species, Breed, Rental


class IndexView(TemplateView):
    """Simple index view"""

    template_name = "cats/index.html"


class AboutView(TemplateView):
    """Simple about view"""

    template_name = "cats/about.html"


class SpeciesListView(ListView):
    """View to choose a Species"""

    model = Species
    template_name = "cats/species.html"


class ExploreFormView(FormView):
    model = Cat
    queryset = Cat.objects.order_by('-name')
    template_name = 'cats/explore_list.html'
    form_class = SearchForm

    def form_valid(self, form):
        context = super().get_context_data()
        date_from = form.cleaned_data["date_from"]
        date_to = form.cleaned_data["date_to"]
        cats_filtered = self.model.objects.get_available_cats(date_from, date_to)
        context['cats_filtered'] = cats_filtered
        return render(self.request, self.template_name, context)


class CatFormView(FormView):
    model = Cat
    template_name = 'cats/cat_list.html'
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Try to get chosen species_id from database. If it won't be found, html will show proper hint
        try:
            species = Species.objects.get(id=self.kwargs['species_id'])
        except Species.DoesNotExist:
            species = None
        context['species'] = species

        return context

    def form_valid(self, form):
        context = super().get_context_data()
        date_from = form.cleaned_data["date_from"]
        date_to = form.cleaned_data["date_to"]

        # Filter out only cats with chosen species_id
        species = Species.objects.get(id=self.kwargs['species_id'])
        species_cats = Cat.objects.filter(breed__species=species)
        cats_filtered = species_cats.get_available_cats(date_from, date_to)

        context['species'] = species
        context['cats_filtered'] = cats_filtered
        return render(self.request, self.template_name, context)


class CatDetailView(DetailView):
    """Detail view for a Cat"""

    model = Cat
    template_name = "cats/details.html"


class RentalFormView(FormView):
    """
    View to let user Rent a Cat, picking proper dates from a RentalForm.

    - On success redirects to "congrats_mail" view.
    - On failure (If Cat isn't available in given dates) renders "rental_dates" view again.

    Picked dates are validated below, but the clean method (dates logic check and availability check)
    is directly in Rental model (works every time, even from admin).
    """

    model = Rental
    template_name = 'cats/rental_form.html'
    form_class = RentalForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = get_object_or_404(Cat, pk=self.kwargs['cat_id'])
        form = RentalForm(
            initial={"cat": cat, "user": self.request.user}, data=self.request.POST or None
        )
        context['cat'] = cat
        context['form'] = form
        return context

    def form_valid(self, form):
        cat = get_object_or_404(Cat, pk=self.kwargs['cat_id'])
        form.initial = {"cat": cat, "user": self.request.user}
        form.data = self.request.POST or None
        form.save()
        return redirect(reverse("cats:congrats_mail", args=[self.kwargs['cat_id']]))


class RentalListView(LoginRequiredMixin, ListView):
    """View to show all user's rentals"""

    model = Rental
    template_name = 'cats/rental_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_rentals = Rental.objects.filter(user=self.request.user).order_by('-rental_date')
        context['user_rentals'] = user_rentals
        return context


@login_required
def rental_congrats_view(request, cat_id):
    """View to send confirmation mail to the user and show him congrats info"""
    cat = get_object_or_404(Cat, pk=cat_id)
    congrats_template = render_to_string(
        "cats/congrats_mail_template.html", {"cat": cat}
    )
    send_mail(
        "Congrats, cat rented!",
        congrats_template,
        "",
        [request.user.email],
        fail_silently=False,
    )
    return render(request, "cats/congrats.html", {"cat": cat})
