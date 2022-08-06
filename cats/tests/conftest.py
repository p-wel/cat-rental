import pytest

from cats.tests.factories import RentalFactory


@pytest.fixture()
def rental_factory_fixture(db):
    """
    Builds Rentals fixture batch with 100 Rental objects
    """
    return RentalFactory.build_batch(100)
