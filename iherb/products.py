import datetime
from typing import Optional
from requests_html import HTML, Element

from iherb.url import IHerbURL
from iherb.utils import parse_html_text_btw


class Product(object):
    def __init__(self,
                 url: str,
                 title: Optional[str] = None,
                 price: Optional[float] = None,
                 price_discount: Optional[float] = None,
                 shipping_saver: Optional[bool] = None,
                 iherb_exclusive: Optional[bool] = None,
                 save_in_cart: Optional[int] = None,
                 in_stock: Optional[bool] = None,
                 special: Optional[bool] = None,
                 trial_product: Optional[bool] = None,
                 rating_count: Optional[int] = None,
                 stars: Optional[float] = None,
                 clearance: Optional[bool] = None,
                 free_shipping_over: Optional[int] = None,
                 best_seller: Optional[bool] = None,
                 loyalty_credit: Optional[int] = None,
                 brand: Optional[str] = None,
                 upc: Optional[str] = None,
                 expiration_date: Optional[datetime.datetime] = None,
                 shipping_weight: Optional[float] = None,
                 package_qty: Optional[str] = None,
                 dimensions: Optional[str] = None):

        self.title = title
        self.url = url
        self.price = price
        self.price_discount = price_discount
        self.shipping_saver = shipping_saver  # if True, better shipping prices
        self.iherb_exclusive = iherb_exclusive  # related to branding?
        self.save_in_cart = save_in_cart  # save 10% in cart
        self.in_stock = in_stock  # or out of stock
        self.special = special  # a special?
        self.trial_product = trial_product  # trial pricing?
        self.rating_count = rating_count  # how many ratings does product have
        self.stars = stars  # how many stars does product have
        self.clearance = clearance  # clearance?
        self.best_seller = best_seller
        self.loyalty_credit = loyalty_credit  # percentage credit
        self.free_shipping_over = free_shipping_over  # some dollar number
        self.brand = brand
        self.upc = upc
        self.expiration_date = expiration_date
        self.shipping_weight = shipping_weight
        self.package_qty = package_qty
        self.dimensions = dimensions

    def __repr__(self):
        return "<Product url: {}>".format(self.url)

    def populate(self) -> "Product":
        iherb_product_url = IHerbURL(self.url)
        r = iherb_product_url.get()
        return self.parse(html=r.html)

    @staticmethod
    def title_parse(element: Element) -> Optional[str]:
        title_element = element.find(".product-title", first=True)
        if title_element:
            return element.find(".product-title", first=True).text

    @staticmethod
    def price_parse(element: Element) -> Optional[float]:
        if element.find("discount-green", first=True):
            if element.find(".price-olp", first=True):
                return float(element.find(".price-olp", first=True).text[1:])
        elif element.find(".price", first=True):
            return float(element.find(".price", first=True).text[1:])

    @staticmethod
    def price_discount_parse(element: Element) -> Optional[float]:
        if element.find("discount-green", first=True):
            if element.find(".discount-green", first=True):
                return float(element.find(".discount-green", first=True).text[1:])
        elif element.find(".price", first=True):
            return float(element.find(".price", first=True).text[1:])

    @staticmethod
    def brand_parse(element: Element) -> Optional[str]:
        brand_element = element.find("#brand", containing="By", first=True)
        if brand_element:
            return brand_element.find("span", first=True).text

    @staticmethod
    def iherb_exclusive_parse(element: Element) -> Optional[bool]:
        if element.find(".product-flag-i-herb-exclusive", containing="iHerb Exclusive", first=True):
            return True

    @staticmethod
    def special_parse(element: Element) -> Optional[bool]:
        if element.find(".product-flag-special", containing="Special", first=True):
            return True

    @staticmethod
    def best_seller_parse(element: Element) -> Optional[bool]:
        if element.find(".product-best-seller", containing="Best Seller", first=True):
            return True

    @staticmethod
    def loyalty_credit_parse(element: Element) -> Optional[int]:
        if element.find(".slanted-container", containing="Loyalty Credit", first=True):
            loyalty_credit_element = element.find(".slanted-container", containing="Loyalty Credit", first=True)
            if loyalty_credit_element:
                return int(loyalty_credit_element.text[:loyalty_credit_element.text.find("% Loyalty Credit")])

    @staticmethod
    def in_stock_parse(element: Element) -> Optional[bool]:
        if element.find(".text-danger", containing="Out of Stock", first=True):
            return False
        elif element.find(".text-primary", containing="In Stock", first=True):
            return True

    @staticmethod
    def free_shipping_over_parse(element: Element) -> Optional[int]:
        free_shipping_over_element = element.find(".text-uppercase", containing="Free Shipping", first=True)
        if free_shipping_over_element:
            return int(free_shipping_over_element.find("bdi", first=True)[1:])

    @staticmethod
    def upc_parse(element: Element) -> Optional[str]:
        upc_element = element.find("li", containing="UPC Code", first=True)
        if upc_element:
            return upc_element.text[upc_element.text.find(": ") + 2:]

    @staticmethod
    def expiration_date_parse(element: Element) -> Optional[datetime.datetime]:
        expiration_date_element = element.find("li", containing="Expiration Date", first=True)
        if expiration_date_element:
            expiration_date = parse_html_text_btw(expiration_date_element.text, "\n?\n", "\n")
            return datetime.datetime.strptime(expiration_date, "%B %Y")

    @staticmethod
    def shipping_weight_parse(element: Element) -> Optional[float]:
        shipping_weight_element = element.find("li", containing="Shipping Weight", first=True)
        if shipping_weight_element:
            shipping_weight, shipping_unit = parse_html_text_btw(shipping_weight_element.text, "\n?\n", "\n").split()
            if shipping_unit == "lbs":
                return float(shipping_weight)

    @staticmethod
    def package_qty_parse(element: Element) -> Optional[str]:
        package_qty_element = element.find("li", containing="Package Quantity", first=True)
        if package_qty_element:
            return package_qty_element.text[package_qty_element.text.find(": ") + 2:]

    @staticmethod
    def dimensions_parse(element: Element) -> Optional[str]:
        dimensions_element = element.find("li", containing="Dimensions", first=True)
        if dimensions_element:
            return parse_html_text_btw(dimensions_element.text, "\n", "\n")

    @staticmethod
    def shipping_saver_parse(element: Element) -> Optional[bool]:
        if element.find(".shipping-saver", containing="Shipping Saver", first=True):
            return True

    @staticmethod
    def save_in_cart_parse(element: Element) -> Optional[int]:
        if element.find("title", containing="in Cart", first=True):
            save_in_cart_element = element.find("title", containing="in Cart", first=True)
            return int(parse_html_text_btw(save_in_cart_element.text, "Save ", "% in Cart"))

    @staticmethod
    def rating_count_parse(element: Element) -> Optional[int]:
        if element.find(".rating-count", first=True):
            rating_count_element = element.find(".rating-count", first=True)
            return int(rating_count_element.find("span", first=True).text)

    @staticmethod
    def stars_parse(element: Element) -> Optional[float]:
        star_len = len("M83.436 10.871c-0.070-0.216-0.271-0.363-0.497-0.363h-9.501l-2.941-9.084c-0.071-0.216-0.271-0.36"
                       "3-0.497-0.364-0.225 0-0.426 0.147-0.496 0.362l-2.958 9.085h-9.484c-0.226 0-0.428 0.148-0.498 0."
                       "363s0.008 0.454 0.189 0.588l7.676 5.623-2.957 9.135c-0.070 0.216 0.006 0.454 0.19 0.589 0.183 0"
                       ".133 0.431 0.133 0.614 0l7.725-5.641 7.709 5.641c0.092 0.067 0.199 0.101 0.307 0.101 0.107 0 0."
                       "215-0.033 0.307-0.101 0.184-0.135 0.26-0.371 0.19-0.589l-2.958-9.134 7.692-5.623c0.183-0.133 0."
                       "259-0.371 0.19-0.588z")

        if element.find("#icon-stars_45"):
            stars_element_container = element.find("#icon-stars_45")
            if stars_element_container.find("path"):  # get length of d
                stars_elements = stars_element_container.find("path")  # get the length of d
                stars = 0
                for star_element in stars_elements:
                    stars += len(star_element.attrs["d"]) / star_len
                return stars

    @staticmethod
    def trial_product_parse(element: Element) -> Optional[bool]:
        if element.find(".product-flag-trial", containing="Trial Product", first=True):
            return True

    @staticmethod
    def clearance_parse(element: Element) -> Optional[bool]:
        if element.find(".product-flag-clearance", containing="Clearance", first=True):
            return True

    def parse(self, html: HTML) -> "Product":

        product = html.find("#product-specs-list", first=True)

        self.title = self.title_parse(product)
        self.price = self.price_parse(product)
        self.price_discount = self.price_discount_parse(product)
        self.shipping_saver = self.shipping_saver_parse(product)
        self.iherb_exclusive = self.iherb_exclusive_parse(product)
        self.free_shipping_over = self.free_shipping_over_parse(product)
        self.save_in_cart = self.save_in_cart_parse(product)
        self.in_stock = self.in_stock_parse(product)
        self.special = self.special_parse(product)
        self.trial_product = self.trial_product_parse(product)
        self.rating_count = self.rating_count_parse(product)
        self.stars = self.stars_parse(product)
        self.clearance = self.clearance_parse(product)
        self.best_seller = self.best_seller_parse(product)
        self.loyalty_credit = self.loyalty_credit_parse(product)
        self.free_shipping_over = self.free_shipping_over_parse(product)
        self.brand = self.brand_parse(product)
        self.upc = self.upc_parse(product)
        self.expiration_date = self.expiration_date_parse(product)
        self.shipping_weight = self.shipping_weight_parse(product)
        self.package_qty = self.package_qty_parse(product)
        self.dimensions = self.dimensions_parse(product)

        return self
