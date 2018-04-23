from typing import Generator

from iherb.products import Product
from iherb.categories import Category


def iherb_products(category: str, limit: int = 0) -> Generator[None, Product, None]:
    """
    yield a populated product from a given category

    :param category: one of Category.categories
    :param limit: integer to limit product results.  0 is no limit.
    :return: yield a Product
    """
    products = 0
    category_pages = Category.get(category)

    for category_page in category_pages:
        for product in category_page:

            yield product.populate()
            products += 1
            if products == limit:
                return None
