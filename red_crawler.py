from html.parser import HTMLParser
from datetime import datetime
from urllib.request import urlopen
import os

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
    red_url = "https://www.reddit.com/"
    categ = "r/EarthPorn"

    if os.path.isfile("red_page"):
        with open("red_page", "r") as html_file:
            html_page = html_file.read()
    else:
        url_obj = urlopen(red_url+categ)
        html_page = str(url_obj.read())

    with open("red_page", "w") as html_file:
        html_file.write(html_page)

    red_parser_obj = RedditEpParser()
    red_parser_obj.feed(html_page)
    post_link = red_parser_obj.link

    red_parser_obj = RedditEpParser()
    img_url = red_url + post_link
    print("Trying to fetch ", img_url)
    url_obj = urlopen(img_url)
    html_page = str(url_obj.read())

    red_parser_obj.feed(html_page)
    img_link = red_parser_obj.link
    print("Trying to fetch ", img_link)
    img_link = urlopen(img_link)

    with open("todays_img.jpg", "wb") as img_file:
        img_file.write(img_link.read())


if __name__ == "__main__":
    main()
