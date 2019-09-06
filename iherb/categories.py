from requests_html import HTML, Element, _NextSymbol, DEFAULT_NEXT_SYMBOL, _Next

from iherb.products import Product
from iherb.url import IHerbURL


# this is the HTML.next method of requests_html with get_next changed
def next(self, fetch: bool = False, next_symbol: _NextSymbol = DEFAULT_NEXT_SYMBOL) -> _Next:
    """Attempts to find the next page, if there is one. If ``fetch``
    is ``True`` (default), returns :class:`HTML <HTML>` object of
    next page. If ``fetch`` is ``False``, simply returns the next URL.
    """

    def get_next():
        url = self.find('.pagination-next', first=True).attrs['href']
        if url:
            return url
        else:
            return None

    __next = get_next()
    if __next:
        url = self._make_absolute(__next)
    else:
        return None

    if fetch:
        return self.session.get(url)
    else:
        return url


# using the altered next function instead of the regular HTML.next method
HTML.next = next


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
            yield Category.parse(html=html)

    @staticmethod
    def parse_url(title: str, element: Element) -> str:
        for i in list(element.absolute_links):
            if title.replace(",", "").replace("'", " ").split()[0] in i and "?" not in i:
                return i
        for j in element.absolute_links:
            print(j)
        raise Exception("did not parse url")

    @staticmethod
    def parse(html: HTML):
        for product in html.find(".product"):
            title = Product.title_parse(product)
            url = Category.parse_url(title=title, element=product)
            showcase_image = Product.showcase_image_parse(element=product)
            price_discount = Product.price_discount_parse(product)
            price = Product.price_parse(product)
            shipping_saver = Product.shipping_saver_parse(product)
            iherb_exclusive = Product.iherb_exclusive_parse(product)
            save_in_cart = Product.save_x_percent_in_cart_parse(product)
            rating_count = Product.rating_count_parse(product)
            stars = Product.stars_parse(product)
            trial_product = Product.trial_product_parse(product)
            clearance = Product.clearance_parse(product)
            in_stock = Product.in_stock_parse(product)
            special = Product.special_parse(product)

            yield Product(url=url,
                          title=title,
                          showcase_image=showcase_image,
                          price_discount=price_discount,
                          price=price,
                          shipping_saver=shipping_saver,
                          iherb_exclusive=iherb_exclusive,
                          save_x_percent_in_cart=save_in_cart,
                          rating_count=rating_count,
                          stars=stars,
                          trial_product=trial_product,
                          clearance=clearance,
                          in_stock=in_stock,
                          special=special)
