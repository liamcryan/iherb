import datetime
from requests_html import HTML

from iherb.url import IHerbURL


class Product(object):
    def __init__(self,
                 title: str,
                 url: str,
                 price: float,
                 upc: str = None,
                 expiration_date: datetime.datetime = None,
                 shipping_weight: float = None,
                 package_qty: str = None,
                 dimensions: str = None):

        self.title = title
        self.url = url
        self.price = price
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

        def parse_html_text_btw(text: str, left: str, right: str) -> str:
            text = text[text.find(left) + len(left):]
            return text[:text.find(right)]

        product = html.find("#product-specs-list", first=True)

        expiration_date_element = product.find("li", containing="Expiration Date", first=True)
        if expiration_date_element:
            expiration_date = parse_html_text_btw(expiration_date_element.text, "\n?\n", "\n")
            self.expiration_date = datetime.datetime.strptime(expiration_date, "%B %Y")

        shipping_weight_element = product.find("li", containing="Shipping Weight", first=True)
        if shipping_weight_element:
            shipping_weight, shipping_unit = parse_html_text_btw(shipping_weight_element.text, "\n?\n", "\n").split()
            if shipping_unit == "lbs":
                self.shipping_weight = float(shipping_weight)

        upc_element = product.find("li", containing="UPC Code", first=True)
        if upc_element:
            self.upc = upc_element.text[upc_element.text.find(": ") + 2:]

        package_qty_element = product.find("li", containing="Package Quantity", first=True)
        if package_qty_element:
            self.package_qty = package_qty_element.text[package_qty_element.text.find(": ") + 2:]

        dimensions_element = product.find("li", containing="Dimensions", first=True)
        if dimensions_element:
            self.dimensions = parse_html_text_btw(dimensions_element.text, "\n", "\n")

        return self
