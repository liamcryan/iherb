from requests_html import HTML, Element

from iherb.products import Product
from iherb.url import IHerbURL


def get_next(html: HTML, next_symbol):
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
            yield Category._parse_one(product)

    @staticmethod
    def _parse_one(product: Element) -> Product:
        title = product.find(".product-title", first=True).text
        url = [i for i in list(product.absolute_links) if "?" not in i][0]
        price = float(product.find(".price", first=True).text[1:])
        return Product(title=title, url=url, price=price)
