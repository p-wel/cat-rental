"""
Views used in cat app
"""

import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView

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


class ExploreListView(ListView):

    def get(self, request, **kwargs):
        cats = None
        page_obj = None
        form = SearchForm(request.GET or None)

        """
        If form is valid, show list.
        If form is not valid, SearchForm will show proper hint
        """
        if form.is_valid():
            date_from = form.cleaned_data["date_from"]
            date_to = form.cleaned_data["date_to"]
            cats = Cat.objects.get_available_cats(date_from, date_to)

            paginator = Paginator(cats, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

        context = {"cats": cats, "form": form, "page_obj": page_obj}
        return render(request, "cats/explore_list.html", context)


class CatListView(ListView):
    """Lists Cats from only one Species"""

    def get(self, request, **kwargs):
        cats = None
        page_obj = None
        form = SearchForm(request.GET or None)
        breeds = Breed.objects.all()

        # If such species id do not exist, then make species=None (html will show proper hint then)
        try:
            species = Species.objects.get(id=self.kwargs['species_id'])
        except Species.DoesNotExist:
            species = None

        # If form is valid, show list. If not, SearchForm will show proper hint
        if form.is_valid():
            date_from = form.cleaned_data["date_from"]
            date_to = form.cleaned_data["date_to"]
            species_cats = Cat.objects.filter(breed__species=species)
            cats = species_cats.get_available_cats(date_from, date_to)

            paginator = Paginator(cats, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

        context = {
            "cats": cats,
            "breeds_list": breeds,
            "form": form,
            "species": species,
            "page_obj": page_obj,
        }
        return render(request, "cats/cat_list.html", context)


class CatDetailView(DetailView):
    """Detail view for a Cat"""

    model = Cat
    template_name = "cats/details.html"


class RentalFormView(FormView, LoginRequiredMixin):
    """
    View to let user Rent a Cat, picking proper dates from a RentalForm.

    - On success redirects to "congrats_mail" view.
    - On failure (If Cat isn't available in given dates) renders "rental_dates" view again.

    Picked dates are validated below, but the clean method (dates logic check and availability check)
    is directly in Rental model (works every time, even from admin).
    """

    def get(self, request, **kwargs):
        cat = get_object_or_404(Cat, pk=self.kwargs['cat_id'])
        rental_form = RentalForm(
            initial={"cat": cat, "user": request.user}, data=request.POST or None
        )
        context = {"cat": cat, "rental_form": rental_form}
        return render(request, "cats/rental_form.html", context)

    def post(self, request, **kwargs):
        cat = get_object_or_404(Cat, pk=self.kwargs['cat_id'])
        rental_form = RentalForm(
            initial={"cat": cat, "user": request.user}, data=request.POST or None
        )
        if request.POST:
            if rental_form.is_valid():
                rental_form.save()
                return redirect(reverse("cats:congrats_mail", args=[self.kwargs['cat_id']]))

        context = {"cat": cat, "rental_form": rental_form}
        return render(request, "cats/rental_form.html", context)


class RentalListView(ListView, LoginRequiredMixin):
    """View to show all user's rentals"""

    def get(self, request, **kwargs):
        user_rentals = Rental.objects.filter(user=request.user).order_by("-rental_date")
        today = datetime.date.today()

        paginator = Paginator(user_rentals, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {"user_rentals": user_rentals, "today": today, "page_obj": page_obj}

        return render(request, "cats/rental_list.html", context)


@login_required
def congrats_mail(request, cat_id):
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
