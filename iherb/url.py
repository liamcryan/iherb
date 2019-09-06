from requests_html import HTMLSession


class IHerbURL(object):
    session = HTMLSession()
    # session.verify = False

    def __init__(self, url):
        self.url = url

    def get(self):
        r = self.session.get(url=self.url)
        if r.ok:
            return r
