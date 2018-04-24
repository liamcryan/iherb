from requests_html import HTML, Element

from iherb.products import Product
from iherb.url import IHerbURL
from iherb.utils import parse_html_text_btw


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

        if product.find("discount-green", first=True):
            price_discount = float(product.find(".discount-green", first=True).text[1:])
            price = float(product.find(".price-olp", first=True).text[1:])
        else:
            price = float(product.find(".price", first=True).text[1:])
            price_discount = price

        free_shipping_over_element = product.find(".text-uppercase", containing="Free Shipping", first=True)
        free_shipping_over = int(free_shipping_over_element.find("bdi", first=True)[1:])

        shipping_saver = True if product.find(".shipping-saver", containing="Shipping Saver", first=True) else False

        iherb_exclusive = True if product.find(".product-flag-i-herb-exclusive", containing="iHerb Exclusive",
                                               first=True) else False

        save_in_cart_element = product.find("title", containing="in Cart", first=True)  # Save 10% in Cart
        save_in_cart = int(parse_html_text_btw(save_in_cart_element.text, "Save ", "% in Cart"))

        in_stock = False if product.find(".out-of-stock-text-nowrap", first=True) else True

        special = True if product.find(".product-flag-special", containing="Special", first=True) else False

        trial_product = True if product.find(".product-flag-trial", containing="Trial Product", first=True) else False

        rating_count_element = product.find(".rating-count", first=True)
        rating_count = int(rating_count_element.find("span", first=True).text)

        stars_element_container = product.find("#icon-stars_45")
        stars_elements = stars_element_container.find("path")  # get length of d
        star_len = len("M83.436 10.871c-0.070-0.216-0.271-0.363-0.497-0.363h-9.501l-2.941-9.084c-0.071-0.216-0.271-0.36"
                       "3-0.497-0.364-0.225 0-0.426 0.147-0.496 0.362l-2.958 9.085h-9.484c-0.226 0-0.428 0.148-0.498 0."
                       "363s0.008 0.454 0.189 0.588l7.676 5.623-2.957 9.135c-0.070 0.216 0.006 0.454 0.19 0.589 0.183 0"
                       ".133 0.431 0.133 0.614 0l7.725-5.641 7.709 5.641c0.092 0.067 0.199 0.101 0.307 0.101 0.107 0 0."
                       "215-0.033 0.307-0.101 0.184-0.135 0.26-0.371 0.19-0.589l-2.958-9.134 7.692-5.623c0.183-0.133 0."
                       "259-0.371 0.19-0.588z")
        stars = 0
        for star_element in stars_elements:
            stars += len(star_element.attrs["d"]) / star_len

        clearance = True if product.find(".product-flag-clearance", containing="Clearance", first=True) else False

        return Product(title=title, url=url,
                       price=price,
                       price_discount=price_discount,
                       shipping_saver=shipping_saver,
                       iherb_exclusive=iherb_exclusive,
                       save_in_cart=save_in_cart,
                       in_stock=in_stock,
                       special=special,
                       trial_product=trial_product,
                       rating_count=rating_count,
                       stars=stars,
                       clearance=clearance,
                       free_shipping_over=free_shipping_over)
