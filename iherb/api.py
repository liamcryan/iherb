from typing import Generator

from iherb.products import Product
from iherb.models import iherb_products


def supplements(limit: int = 0) -> Generator[Product, None, None]:
    return iherb_products("supplements", limit)


def bath_beauty(limit: int = 0) -> Generator[Product, None, None]:
    return iherb_products("bath-beauty", limit)


def sports_fitness_athletic(limit: int = 0) -> Generator[Product, None, None]:
    return iherb_products("sports-fitness-athletic", limit)


def grocery(limit: int = 0) -> Generator[Product, None, None]:
    return iherb_products("Grocery", limit)


def baby_kids(limit: int = 0) -> Generator[Product, None, None]:
    return iherb_products("baby-kids", limit)


def pets(limit: int = 0) -> Generator[Product, None, None]:
    return iherb_products("pets", limit)


def healthy_home(limit: int = 0) -> Generator[Product, None, None]:
    return iherb_products("healthy-home", limit)


if __name__ == "__main__":
    for i in supplements(limit=0):
        pass
        # print(i)
