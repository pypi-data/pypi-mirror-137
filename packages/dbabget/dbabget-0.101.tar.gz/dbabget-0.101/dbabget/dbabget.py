import argparse

from .douban_spider import (
    html_downloader,
    html_outputer,
    html_parser,
    url_manger,
)


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manger.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url, album_name):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print("爬取第 %d 页: %s" % (count, new_url))
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont, album_name)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)

                if count == 10:
                    break
                count = count + 1
            except Exception as e:
                raise e
                print(f"craw failed {e}")

        self.outputer.output_html()


def main():
    parser = argparse.ArgumentParser("豆瓣相册下载器")
    parser.add_argument(
        "album_id",
        type=str,
        default=None,
        help="要下载的豆瓣相册ID(例如: 1639309626)",
    )
    parser.add_argument(
        "-n",
        dest="album_name",
        type=str,
        default=None,
        help="相册名称",
    )
    args = parser.parse_args()

    if not args.album_id:
        raise ValueError("请输入相册ID")
    if not args.album_name:
        album_name = input("请输入相册名称(例如: xxxx相册, 可按 Enter跳过): ")
        if not album_name or album_name == "":
            album_name = args.album_id
    else:
        album_name = args.album_name

    root_url = "https://www.douban.com/photos/album/" + args.album_id + "/"
    print("即将开始下载相册: %s " % root_url)

    obj_spider = SpiderMain()
    obj_spider.craw(root_url, album_name)


if __name__ == "__main__":
    main()
