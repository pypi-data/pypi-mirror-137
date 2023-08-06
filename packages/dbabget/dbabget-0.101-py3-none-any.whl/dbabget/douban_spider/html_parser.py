from bs4 import BeautifulSoup
import re
import urllib.parse
import urllib.request
from pathlib import Path


class HtmlParser(object):
    def _get_new_urls(self, page_url, soup, album_name):
        photo_dir = Path(f"./{album_name}")
        photo_dir.mkdir(parents=True, exist_ok=True)
        new_urls = set()
        wrap_links = soup.find_all("a", {"class": "photolst_photo"})
        links = [_link.find("img") for _link in wrap_links]
        print(f"共计有{len(links)}张图片")
        opener = urllib.request.build_opener()
        opener.addheaders = [
            (
                "User-agent",
                " Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0",
            )
        ]
        urllib.request.install_opener(opener)
        for link in links:
            photo_url = link["src"].replace("/m/", "/l/")  # 替换 middle to large

            photo_name = re.search(r"p[0-9]+.jpg$", photo_url).group(0)

            print(f"正在下载图片 {photo_name}")
            urllib.request.urlretrieve(photo_url, photo_dir / photo_name)

        paginator = soup.find_all("div", {"class": "paginator"})
        try:
            new_urls = [
                str(p.find("span", {"class": "next"}).find("a")["href"])
                for p in paginator
            ]
            return new_urls
        except TypeError:
            return []
        except Exception as e:
            raise e

    def _get_new_data(self, page_url, soup):
        res_data = {}
        res_data["url"] = page_url
        return res_data

    def parse(self, page_url, html_cont, album_name):
        if page_url is None or len(html_cont) == 0:
            return None
        soup = BeautifulSoup(html_cont, "html.parser", from_encoding="urf-8")
        new_urls = self._get_new_urls(page_url, soup, album_name)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
