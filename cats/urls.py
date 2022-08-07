"""
Urls for cats app
"""

from django.urls import path

from cats.views import (
    rental_congrats_view,
    IndexView,
    AboutView,
    SpeciesListView,
    CatDetailView,
    RentalFormView,
    RentalListView,
    CatFormView,
    ExploreFormView,
)

app_name = "cats"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("species/", SpeciesListView.as_view(), name="species"),
    path("explore/", ExploreFormView.as_view(), name="explore_list"),
    path("species/<int:species_id>/", CatFormView.as_view(), name="cats_list"),
    path("cat/<int:pk>/", CatDetailView.as_view(), name="details"),
    path("cat/<int:cat_id>/rental_dates/", RentalFormView.as_view(), name="rental_dates"),
    path("cat/<int:cat_id>/rental_dates/congrats/", rental_congrats_view, name="congrats_mail"),
    path("cat/rentals/", RentalListView.as_view(), name="rentals_history"),
]
