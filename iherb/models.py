from iherb.categories import Category


def iherb_products(category: str, limit: int, product_details: bool):
    """
    yield a populated product from a given category

    :param category: one of Category.categories
    :param limit: integer to limit product results.  0 is no limit.
    :param product_details: bool to get the actual details of the product rather than superficial details such as title,
                            url, etc
    :return: yield a Product
    """
    products = 0
    category_pages = Category.get(category=category)

    for category_page in category_pages:
        for product in category_page:

            if product_details:
                yield product.populate()

                products += 1
                if products == limit:
                    return None
