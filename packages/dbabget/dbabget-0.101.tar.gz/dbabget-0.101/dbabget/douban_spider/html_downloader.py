# from urllib import request
import urllib.request


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None

        req = urllib.request.Request(
            url=url,
            headers={
                "User-Agent": " Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0"
            },
        )
        response = urllib.request.urlopen(req)

        if response.getcode() != 200:
            return None
        return response.read()
