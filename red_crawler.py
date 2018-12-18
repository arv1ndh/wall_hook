from html.parser import HTMLParser
from datetime import datetime
from urllib.request import urlopen,Request
import os

custom_header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

class RedditEpParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.post_s_flag = 0
        self.link = ""

    def handle_starttag(self, tag, attrs):
        if 'img' == tag and len(attrs):
            if attrs[0][0] == 'src' and 'renderTimingPixel' in attrs[0][1]:
                self.post_s_flag = 1

        if 'a' == tag and self.post_s_flag == 1:
            if attrs[0][1].startswith("/r") and "comments" in attrs[0][1]:
                if not len(self.link):
                    self.link = attrs[0][1]
            elif attrs[0][1].endswith("jpg") or attrs[0][1].endswith("png"):
                if not len(self.link):
                    self.link = attrs[0][1]

def main():
    red_url = "https://www.reddit.com"
    categ = "/r/EarthPorn"

    print("Trying to fetch ", red_url+categ)
    url_obj = urlopen(Request(red_url+categ, headers=custom_header))
    html_page = str(url_obj.read())

    red_parser_obj = RedditEpParser()
    red_parser_obj.feed(html_page)
    post_link = red_parser_obj.link
    print("Obtained the post link ", post_link)

    red_parser_obj = RedditEpParser()
    img_url = red_url + post_link
    print("Trying to fetch ", img_url)
    url_obj = urlopen(Request(img_url, headers = custom_header))
    html_page = str(url_obj.read())
    print(html_page)

    red_parser_obj.feed(html_page)
    img_link = red_parser_obj.link
    print("Trying to download ", img_link)
    img_link = urlopen(Request(img_link, headers = custom_header))

    with open("todays_img.jpg", "wb") as img_file:
        img_file.write(img_link.read())
    print("Image Downloaded successfully")


if __name__ == "__main__":
    main()
