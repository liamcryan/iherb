from iherb.categories import Category


def iherb_products(category: str, limit: int = 0, minimize_footprint: bool = True):
    """
    yield a populated product from a given category

    :param category: one of Category.categories
    :param limit: integer to limit product results.  0 is no limit.
    :param minimize_footprint: bool to limit or not limit http requests
    :return: yield a Product
    """
    products = 0
    category_pages = Category.get(category)

    for category_page in category_pages:
        for product in category_page:

            if not minimize_footprint:
                yield product.populate()

                products += 1
                if products == limit:
                    return None
