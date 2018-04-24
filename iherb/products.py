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
    def brand_parse(element: Element) -> str:
        brand_element = element.find("#brand", containing="By", first=True)
        if brand_element:
            return brand_element.find("span", first=True).text

    @staticmethod
    def clearance_parse(element: Element) -> bool:
        if element.find(".product-flag-clearance", containing="clearance", first=True):
            return True
        return False

    @staticmethod
    def iherb_exclusive_parse(element: Element) -> bool:
        if element.find(".product-flag-i-herb-exclusive", containing="iHerb Exclusive", first=True):
            return True
        return False

    @staticmethod
    def special_parse(element: Element) -> bool:
        if element.find(".product-flag-special", containing="Special", first=True):
            return True
        return False

    @staticmethod
    def best_seller_parse(element: Element) -> bool:
        if element.find(".product-best-seller", containing="Best Seller", first=True):
            return True
        return False

    @staticmethod
    def loyalty_credit_parse(element: Element) -> int:
        if element.find(".slanted-container", containing="Loyalty Credit", first=True):
            loyalty_credit_element = element.find(".slanted-container", containing="Loyalty Credit", first=True)
            if loyalty_credit_element:
                return int(loyalty_credit_element.text[:loyalty_credit_element.text.find("% Loyalty Credit")])
        return 0

    @staticmethod
    def in_stock_parse(element: Element) -> bool:
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

    def parse(self, html: HTML) -> "Product":

        product = html.find("#product-specs-list", first=True)

        # todo price

        # todo url

        # todo title

        # todo price discount

        # todo shipping saver

        self.iherb_exclusive = self.iherb_exclusive_parse(product)

        # todo save in cart

        self.in_stock = self.in_stock_parse(product)

        self.special = self.special_parse(product)

        # todo trial product

        # todo rating count

        # todo stars

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
