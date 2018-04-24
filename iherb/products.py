import datetime
from requests_html import HTML

from iherb.url import IHerbURL
from iherb.utils import parse_html_text_btw


class Product(object):
    def __init__(self,
                 title: str,
                 url: str,
                 price: float,
                 price_discount: float,
                 shipping_saver: bool,
                 iherb_exclusive: bool,
                 save_in_cart: int,
                 in_stock: bool,
                 special: bool,
                 trial_product: bool,
                 rating_count: int,
                 stars: float,
                 clearance: bool,
                 free_shipping_over: int,
                 best_seller: bool = False,
                 loyalty_credit: int = 0,
                 brand: str = None,
                 upc: str = None,
                 expiration_date: datetime.datetime = None,
                 shipping_weight: float = None,
                 package_qty: str = None,
                 dimensions: str = None):

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
        return "<Product UPC{} ${}>".format(self.upc, self.price)

    def populate(self) -> "Product":
        iherb_product_url = IHerbURL(self.url)
        r = iherb_product_url.get()
        return self.parse(html=r.html)

    def parse(self, html: HTML) -> "Product":

        product = html.find("#product-specs-list", first=True)

        brand_element = product.find("#brand", containing="By", first=True)
        if brand_element:
            self.brand = brand_element.find("span", first=True).text

        if product.find(".product-flag-clearance", containing="clearance", first=True):
            self.clearance = True
        else:
            self.clearance = False

        if product.find(".product-flag-i-herb-exclusive", containing="iHerb Exclusive", first=True):
            self.iherb_exclusive = True
        else:
            self.iherb_exclusive = False

        if product.find(".product-flag-special", containing="Special", first=True):
            self.special = True
        else:
            self.special = False

        if product.find(".product-best-seller", containing="Best Seller", first=True):
            self.best_seller = True
        else:
            self.best_seller = False

        if product.find(".slanted-container", containing="Loyalty Credit", first=True):
            loyalty_credit_element = product.find(".slanted-container", containing="Loyalty Credit", first=True)
            self.loyalty_credit = int(loyalty_credit_element.text[:loyalty_credit_element.text.find(
                "% Loyalty Credit")])

        if product.find(".text-danger", containing="Out of Stock", first=True):
            self.in_stock = False
        elif product.find(".text-primary", containing="In Stock", first=True):
            self.in_stock = True

        free_shipping_over_element = product.find(".text-uppercase", containing="Free Shipping", first=True)
        if free_shipping_over_element:
            self.free_shipping_over = int(free_shipping_over_element.find("bdi", first=True)[1:])

        upc_element = product.find("li", containing="UPC Code", first=True)
        if upc_element:
            self.upc = upc_element.text[upc_element.text.find(": ") + 2:]

        expiration_date_element = product.find("li", containing="Expiration Date", first=True)
        if expiration_date_element:
            expiration_date = parse_html_text_btw(expiration_date_element.text, "\n?\n", "\n")
            self.expiration_date = datetime.datetime.strptime(expiration_date, "%B %Y")

        shipping_weight_element = product.find("li", containing="Shipping Weight", first=True)
        if shipping_weight_element:
            shipping_weight, shipping_unit = parse_html_text_btw(shipping_weight_element.text, "\n?\n", "\n").split()
            if shipping_unit == "lbs":
                self.shipping_weight = float(shipping_weight)

        package_qty_element = product.find("li", containing="Package Quantity", first=True)
        if package_qty_element:
            self.package_qty = package_qty_element.text[package_qty_element.text.find(": ") + 2:]

        dimensions_element = product.find("li", containing="Dimensions", first=True)
        if dimensions_element:
            self.dimensions = parse_html_text_btw(dimensions_element.text, "\n", "\n")

        return self
