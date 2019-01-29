from html.parser import HTMLParser
from datetime import datetime
from urllib.request import urlopen,Request
import os
import re

custom_header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
REQ_IMG_H = 1080
REQ_IMG_W = 1920

class RedditEpParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.post_s_flag = 0
        self.img_flag = 0
        self.link = ""
        self.regex = re.compile("[\[,\(]\d*x\d*[\],\)]")
        self.final_link = ""

    def handle_starttag(self, tag, attrs):
        if 'h2' == tag and len(attrs) and "imors3-" in attrs[0][1]:
            self.post_s_flag = 1

        if 'a' == tag and self.post_s_flag == 1:
            if len(attrs) > 2 and attrs[2][1].startswith("/r") and "comments" in attrs[2][1]:
                self.link = attrs[2][1]
            elif attrs[0][1].endswith("jpg") or attrs[0][1].endswith("png"):
                print(attrs)
                self.link = attrs[0][1]
                self.img_flag = 1

    def handle_data(self, data):
        global REQ_IMG_H, REQ_IMG_W
        if self.link != "" and self.img_flag == 0:
            result = self.regex.search(data)
            if result is None:
                self.link = ""
                return
            resol_string = result.group()
            resol_string = resol_string[1:-1]
            width, height = map(int, resol_string.split('x'))
            if width >= height and height >= REQ_IMG_H and width >= REQ_IMG_W:
                REQ_IMG_H = height
                REQ_IMG_W = width
                self.final_link = self.link
            self.link = ""

def red_crawler():
    red_url = "https://www.reddit.com"
    categ = "/r/EarthPorn"

    print("Trying to fetch ", red_url+categ)
    url_obj = urlopen(Request(red_url+categ, headers=custom_header))
    html_page = str(url_obj.read())

    red_parser_obj = RedditEpParser()
    red_parser_obj.feed(html_page)
    post_link = red_parser_obj.final_link
    if post_link is None:
        print("No high res image found, exiting")
        import sys
        sys.exit()
    print("Obtained the post link ", post_link)

    red_parser_obj = RedditEpParser()
    img_url = red_url + post_link
    print("Trying to fetch ", img_url)
    url_obj = urlopen(Request(img_url, headers = custom_header))
    html_page = str(url_obj.read())

    red_parser_obj.feed(html_page)
    img_link = red_parser_obj.link
    print("Trying to download ", img_link)
    img_link_obj = urlopen(Request(img_link, headers = custom_header))

    img_name = "todays_" + img_link.split('/')[-1]
    with open(img_name, "wb") as img_file:
        img_file.write(img_link_obj.read())
    print("Image Downloaded successfully")
    return img_name

def main():
    red_crawler()

if __name__ == "__main__":
    main()
