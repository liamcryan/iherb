from requests_html import HTMLSession


class IHerbURL(object):
    headers = {"user-agent": "Mozilla/5.0 "
                             "(Windows NT 6.1; WOW64) "
                             "AppleWebKit/537.36 "
                             "(KHTML, like Gecko) "
                             "Chrome/66.0.3359.117 Safari/537.36"
               }

    def __init__(self, url):
        self.url = url

    def get(self):
        session = HTMLSession()
        r = session.get(url=self.url, headers=self.headers)
        if r.ok:
            return r
        