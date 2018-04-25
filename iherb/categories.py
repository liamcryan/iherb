from typing import Optional
from requests_html import HTML

from iherb.products import Product
from iherb.url import IHerbURL


def get_next(html: HTML, next_symbol: None) -> Optional[str]:
    url = html.find('.pagination-next', first=True).attrs['href']
    if url:
        return url
    else:
        return None


HTML.get_next = get_next


class Category(object):
    """
    Category.get(category="supplements")  # yield all Products in "supplements"

    """

    base_url = "https://www.iherb.com/c/"

    categories = ["supplements",
                  "bath-beauty",
                  "sports-fitness-athletic",
                  "Grocery",
                  "baby-kids",
                  "pets",
                  "healthy-home"]

    @staticmethod
    def get(category: str):
        if category not in Category.categories:
            raise Exception("not a valid category")

        iherb_category_url = IHerbURL(url=Category.base_url + category)
        response = iherb_category_url.get()

        for html in response.html:
            print(html.url)
            yield Category.parse(html=html)

    @staticmethod
    def parse(html: HTML):
        for product in html.find(".product-inner"):

            url = [i for i in list(product.absolute_links) if "?" not in i][0]
            title = Product.title_parse(product)
            price_discount = Product.price_discount_parse(product)
            price = Product.price_parse(product)
            free_shipping_over = Product.free_shipping_over_parse(product)
            shipping_saver = Product.shipping_saver_parse(product)
            iherb_exclusive = Product.iherb_exclusive_parse(product)
            save_in_cart = Product.save_in_cart_parse(product)
            rating_count = Product.rating_count_parse(product)
            stars = Product.stars_parse(product)
            trial_product = Product.trial_product_parse(product)
            clearance = Product.clearance_parse(product)
            in_stock = Product.in_stock_parse(product)
            special = Product.special_parse(product)

            yield Product(url=url,
                          title=title,
                          price_discount=price_discount,
                          price=price,
                          free_shipping_over=free_shipping_over,
                          shipping_saver=shipping_saver,
                          iherb_exclusive=iherb_exclusive,
                          save_in_cart=save_in_cart,
                          rating_count=rating_count,
                          stars=stars,
                          trial_product=trial_product,
                          clearance=clearance,
                          in_stock=in_stock,
                          special=special)
