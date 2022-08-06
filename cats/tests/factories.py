import datetime

import factory
from django.contrib.auth.models import User
from factory.fuzzy import FuzzyInteger
from faker import Factory

from cats.models import Rental, Species, Breed, Cat

faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Sequence(lambda n: f"user_{n}@p-wel_cat_rental.pl")
    password = "password123"


class SpeciesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Species

    name = factory.Sequence(lambda n: f"Species_{n}")
    description = factory.Sequence(lambda n: f"Species_description_{n}")


class BreedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Breed

    name = factory.Sequence(lambda n: f"Breed_{n}")
    description = factory.Sequence(lambda n: f"Breed_description_{n}")
    species = factory.SubFactory(SpeciesFactory)


class CatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cat

    name = factory.Sequence(lambda n: f"Cat_{n}")
    breed = factory.SubFactory(BreedFactory)
    description = factory.Sequence(lambda n: f"Cat_description_{n}")


class RentalFactory(factory.django.DjangoModelFactory):
    """
    RentalFactory firstly creates new objects:
    - Species
    - Breed
    - Cat
    - User
    Then uses them to create a new Rental object with 30-days rental period
    """

    _rentals_first_status = Rental.STATUS[0][0]
    _rentals_last_status = Rental.STATUS[len(Rental.STATUS) - 1][0]

    class Meta:
        model = Rental

    cat = factory.SubFactory(CatFactory)
    user = factory.SubFactory(UserFactory)
    rental_date = factory.LazyAttribute(lambda _: faker.future_date())
    return_date = factory.LazyAttribute(lambda _self: _self.rental_date + datetime.timedelta(days=30))

    status = FuzzyInteger(_rentals_first_status, _rentals_last_status, 1)
