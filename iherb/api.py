from typing import Generator

from iherb.products import Product
from iherb.models import iherb_products


def supplements(limit: int = 0, minimize_footprint: bool = False):
    return iherb_products("supplements", limit, minimize_footprint)


def bath_beauty(limit: int = 0, minimize_footprint: bool = False):
    return iherb_products("bath-beauty", limit, minimize_footprint)


def sports_fitness_athletic(limit: int = 0, minimize_footprint: bool = False):
    return iherb_products("sports-fitness-athletic", limit, minimize_footprint)


def grocery(limit: int = 0, minimize_footprint: bool = False):
    return iherb_products("Grocery", limit, minimize_footprint)


def baby_kids(limit: int = 0, minimize_footprint: bool = False):
    return iherb_products("baby-kids", limit, minimize_footprint)


def pets(limit: int = 0, minimize_footprint: bool = False):
    return iherb_products("pets", limit, minimize_footprint)


def healthy_home(limit: int = 0, minimize_footprint: bool = False):
    return iherb_products("healthy-home", limit, minimize_footprint)


if __name__ == "__main__":
    for i in supplements(limit=10):
        pass
        # print(i)
