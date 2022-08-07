"""
Admin for CRUD on objects creating in app
"""
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Cat, Species, Breed, Rental


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    """Register admin for Cats"""

    list_display = ["id", "name", "breed"]
    search_fields = ["id", "breed"]


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    """Register admin for Species"""

    list_display = ["id", "name"]
    search_fields = ["id", "name"]


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    """Register admin for Breeds"""

    list_display = ["id", "name", "species"]
    search_fields = ["id", "name"]
    list_filter = ["species"]


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    """Register admin for Rentals"""

    @admin.action(description="Update status")
    def update_status(self, request, queryset):
        if "submit" in request.POST:
            queryset.update(status=request.POST["options"][1])

            self.message_user(request, f"Changed status for {queryset.count()} rentals")
            return HttpResponseRedirect(request.get_full_path())

        return render(
            request,
            "admin/action_update_status.html",
            context={"rentals": queryset, "status_options": Rental.STATUS},
        )

    list_display = ["id", "user", "cat", "rental_date", "return_date", "status"]
    list_filter = ["status", "rental_date", "return_date"]
    search_fields = ["id", "cat__name", "user__username"]
    actions = [
        update_status,
    ]
