"""
Urls for cats app
"""

from django.urls import path

from cats.views import (
    congrats_mail,
    IndexView,
    AboutView,
    SpeciesListView,
    # rentals_history,
    CatDetailView,
    ExploreListView,
    CatListView,
    RentalFormView,
    RentalListView,
)

app_name = "cats"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("species/", SpeciesListView.as_view(), name="species"),
    path("explore/", ExploreListView.as_view(), name="explore_list"),
    path("species/<int:species_id>/", CatListView.as_view(), name="cats_list"),
    path("cat/<int:pk>/", CatDetailView.as_view(), name="details"),
    path("cat/<int:cat_id>/rental_dates/", RentalFormView.as_view(), name="rental_dates"),
    path("cat/<int:cat_id>/rental_dates/congrats/", congrats_mail, name="congrats_mail"),
    # path("cat/rentals/", rentals_history, name="rentals_history"),
    path("cat/rentals/", RentalListView.as_view(), name="rentals_history"),
]
