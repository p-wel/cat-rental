import datetime

from cats.models import Rental


def test_rental_has_user_assigned(db, rental_factory_fixture):
    """
    Test if rental has user assigned
    """

    for rental in rental_factory_fixture:
        assert rental.user is not None


def test_rental_has_cat_assigned(db, rental_factory_fixture):
    """
    Test if rental has cat assigned
    """

    for rental in rental_factory_fixture:
        assert rental.cat is not None


def test_rental_has_proper_dates(db, rental_factory_fixture):
    """
    Test if rentals have rental date lower or equal to return date
    """

    for rental in rental_factory_fixture:
        assert rental.rental_date <= rental.return_date


def test_rental_dates_are_not_none(db, rental_factory_fixture):
    """
    Test if rental dates are not None
    """

    for rental in rental_factory_fixture:
        assert rental.rental_date is not None and rental.return_date is not None


def test_rental_dates_are_date_types(db, rental_factory_fixture):
    """
    Test if rental dates are 'datetime.date' type
    """

    for rental in rental_factory_fixture:
        assert (
            type(rental.rental_date) is datetime.date
            and type(rental.return_date) is datetime.date
        )
