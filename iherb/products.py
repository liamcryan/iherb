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
                 showcase_image: Optional[float] = None,
                 price_discount: Optional[float] = None,
                 shipping_saver: Optional[bool] = None,
                 iherb_exclusive: Optional[bool] = None,
                 save_x_percent_in_cart: Optional[int] = None,
                 in_stock: Optional[bool] = None,
                 special: Optional[bool] = None,
                 trial_product: Optional[bool] = None,
                 rating_count: Optional[int] = None,
                 stars: Optional[float] = None,
                 clearance: Optional[bool] = None,
                 free_shipping_over_x_dollars: Optional[int] = None,
                 best_seller: Optional[bool] = None,
                 loyalty_credit_x_percent: Optional[int] = None,
                 brand: Optional[str] = None,
                 product_code: Optional[str] = None,
                 upc: Optional[str] = None,
                 expiration_date: Optional[datetime.datetime] = None,
                 shipping_weight: Optional[float] = None,
                 package_qty: Optional[str] = None,
                 dimensions: Optional[str] = None):

        self.title = title
        self.url = url
        self.price = price
        self.showcase_image = showcase_image
        self.price_discount = price_discount
        self.shipping_saver = shipping_saver  # if True, better shipping prices
        self.iherb_exclusive = iherb_exclusive  # related to branding?
        self.save_x_percent_in_cart = save_x_percent_in_cart  # save 10% in cart
        self.in_stock = in_stock  # or out of stock
        self.special = special  # a special?
        self.trial_product = trial_product  # trial pricing?
        self.rating_count = rating_count  # how many ratings does product have
        self.stars = stars  # how many stars does product have
        self.clearance = clearance  # clearance?
        self.best_seller = best_seller
        self.loyalty_credit_x_percent = loyalty_credit_x_percent  # percentage credit
        self.free_shipping_over_x_dollars = free_shipping_over_x_dollars  # some dollar number
        self.brand = brand
        self.product_code = product_code  # iherb special code
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
            return title_element.text
        title_element = element.find("#name", first=True)
        if title_element:
            return title_element.text

    @staticmethod
    def price_parse(element: Element) -> Optional[float]:
        if element.find("discount-green", first=True):
            if element.find(".price-olp", first=True):
                return float(element.find(".price-olp", first=True).text[1:])
        elif element.find(".price", first=True):
            return float(element.find(".price", first=True).text[1:])

    @staticmethod
    def showcase_image_parse(element: Element) -> Optional[str]:
        showcase_image_element = element.find("img", first=True)
        if showcase_image_element:
            return showcase_image_element.attrs["src"]

    @staticmethod
    def price_discount_parse(element: Element) -> Optional[float]:
        if element.find(".discount-green", first=True):
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
    def loyalty_credit_x_percent_parse(element: Element) -> Optional[int]:
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
    def free_shipping_over_x_dollars_parse(element: Element) -> Optional[int]:
        free_shipping_over_element = element.find(".banner-alert", first=True)
        if free_shipping_over_element:
            if "Free Shipping\xa0for orders over" in free_shipping_over_element.text:
                return int(free_shipping_over_element.text[free_shipping_over_element.text.find("\n") + 2:])

    @staticmethod
    def upc_parse(element: Element) -> Optional[str]:
        upc_element = element.find("li", containing="UPC Code", first=True)
        if upc_element:
            return upc_element.text[upc_element.text.find(": ") + 2:]

    @staticmethod
    def product_code_parse(element: Element) -> Optional[str]:
        product_code_element = element.find("li", containing="Product Code", first=True)
        if product_code_element:
            return product_code_element.text[product_code_element.text.find(": ") + 2:]

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
    def save_x_percent_in_cart_parse(element: Element) -> Optional[int]:
        if element.find("title", containing="in Cart", first=True):
            save_x_percent_in_cart_element = element.find("title", containing="in Cart", first=True)
            return int(parse_html_text_btw(save_x_percent_in_cart_element.text, "Save ", "% in Cart"))

    @staticmethod
    def rating_count_parse(element: Element) -> Optional[int]:
        if element.find(".rating-count", first=True):
            rating_count_element = element.find(".rating-count", first=True)
            return int(rating_count_element.find("span", first=True).text)

    @staticmethod
    def stars_parse(element: Element) -> Optional[float]:
        stars_element = element.find(".stars", first=True)
        if stars_element:
            stars = stars_element.attrs["title"]
            return float(stars[:stars.find("/5")])

    @staticmethod
    def trial_product_parse(element: Element) -> Optional[bool]:
        if element.find(".product-flag-trial", containing="Trial Product", first=True):
            return True

    @staticmethod
    def clearance_parse(element: Element) -> Optional[bool]:
        if element.find(".product-flag-clearance", containing="Clearance", first=True):
            return True

    def parse(self, html: HTML) -> "Product":

        # product = html.find("#product-specs-list", first=True)
        product = html.find("body", first=True)

        if self.title is None:
            self.title = self.title_parse(product)
        if self.price is None:
            self.price = self.price_parse(product)
        if self.price_discount is None:
            self.price_discount = self.price_discount_parse(product)
        if self.showcase_image is None:
            self.showcase_image = self.showcase_image_parse(product)
        if self.shipping_saver is None:
            self.shipping_saver = self.shipping_saver_parse(product)
        if self.iherb_exclusive is None:
            self.iherb_exclusive = self.iherb_exclusive_parse(product)
        if self.free_shipping_over_x_dollars is None:
            self.free_shipping_over_x_dollars = self.free_shipping_over_x_dollars_parse(product)
        if self.save_x_percent_in_cart is None:
            self.save_x_percent_in_cart = self.save_x_percent_in_cart_parse(product)
        if self.in_stock is None:
            self.in_stock = self.in_stock_parse(product)
        if self.special is None:
            self.special = self.special_parse(product)
        if self.trial_product is None:
            self.trial_product = self.trial_product_parse(product)
        if self.rating_count is None:
            self.rating_count = self.rating_count_parse(product)
        if self.stars is None:
            self.stars = self.stars_parse(product)
        if self.clearance is None:
            self.clearance = self.clearance_parse(product)
        if self.best_seller is None:
            self.best_seller = self.best_seller_parse(product)
        if self.loyalty_credit_x_percent is None:
            self.loyalty_credit_x_percent = self.loyalty_credit_x_percent_parse(product)
        if self.free_shipping_over_x_dollars is None:
            self.free_shipping_over_x_dollars = self.free_shipping_over_x_dollars_parse(product)
        if self.brand is None:
            self.brand = self.brand_parse(product)
        if self.upc is None:
            self.upc = self.upc_parse(product)
        if self.product_code is None:
            self.product_code = self.product_code_parse(product)
        if self.expiration_date is None:
            self.expiration_date = self.expiration_date_parse(product)
        if self.shipping_weight is None:
            self.shipping_weight = self.shipping_weight_parse(product)
        if self.package_qty is None:
            self.package_qty = self.package_qty_parse(product)
        if self.dimensions is None:
            self.dimensions = self.dimensions_parse(product)

        return self
