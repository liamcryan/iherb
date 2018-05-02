from typing import Generator

from iherb.products import Product
from iherb.models import iherb_products


def supplements(limit: int = 0, product_details: bool = True):
    return iherb_products("supplements", limit, product_details)


def bath_beauty(limit: int = 0, product_details: bool = True):
    return iherb_products("bath-beauty", limit, product_details)


def sports_fitness_athletic(limit: int = 0, product_details: bool = True):
    return iherb_products("sports-fitness-athletic", limit, product_details)


def grocery(limit: int = 0, product_details: bool = True):
    return iherb_products("Grocery", limit, product_details)


def baby_kids(limit: int = 0, product_details: bool = True):
    return iherb_products("baby-kids", limit, product_details)


def pets(limit: int = 0, product_details: bool = True):
    return iherb_products("pets", limit, product_details)


def healthy_home(limit: int = 0, product_details: bool = True):
    return iherb_products("healthy-home", limit, product_details)


if __name__ == "__main__":
    for i in supplements(limit=10, product_details=True):
        print(i)
