"""
Models used in app
"""
import datetime

from django.core.exceptions import ValidationError
from django.db import models


class CatQuerySet(models.QuerySet):
    def get_available_cats(self, rental_date, return_date):
        """
        Method in Cat QuerySet to filter out rented cats.

        Returns a list of cats available between given dates.
        """

        return self.exclude(
            rentals__rental_date__gte=rental_date, rentals__return_date__lte=return_date
        )


class Cat(models.Model):
    """Basic class for Cat objects"""

    name = models.CharField(max_length=50)
    breed = models.ForeignKey("cats.Breed", on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    objects = CatQuerySet.as_manager()

    def __str__(self):
        return f"{self.name} (ID: {self.id})"


class Breed(models.Model):
    """Basic class for Breed objects"""

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    species = models.ForeignKey("cats.Species", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Species(models.Model):
    """Basic class for Species objects"""

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Species"

    def __str__(self):
        return self.name


class Rental(models.Model):
    """Basic class for Rental objects"""

    NOT_ACTIVE = 0
    PENDING = 1
    ACTIVE = 2
    FINISHED = 3
    CANCELLED = 4
    STATUS = (
        (NOT_ACTIVE, "Not activate (draft)"),
        (PENDING, "Pending (@)"),
        (ACTIVE, "Active"),
        (FINISHED, "Finished"),
        (CANCELLED, "Cancelled"),
    )
    cat = models.ForeignKey("Cat", on_delete=models.CASCADE, related_name="rentals")
    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="rentals"
    )
    rental_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        choices=STATUS,
        default=ACTIVE,
    )

    def clean(self):
        super().clean()
        if self.rental_date < datetime.date.today():
            raise ValidationError("Cannot pick date from the past")
        if self.rental_date > self.return_date:
            raise ValidationError('"Return date" must be further than "return from"')

        # If cat won't be found in available cats queryset - raise error
        if not Cat.objects.get_available_cats(
            self.rental_date, self.return_date
        ).filter(pk=self.cat.pk):
            raise ValidationError("Cat is not available in given timeframes")

    def __str__(self):
        return f"Rental {self.id} ({self.cat.name})"
