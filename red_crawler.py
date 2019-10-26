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
        if 'a' == tag and len(attrs) > 2 and ("data-click-id","body") in attrs:
            t_link = dict(attrs)["href"]
            if "EarthPorn/comments" in t_link:
                self.link = t_link
            elif t_link.endswith("jpg") or t_link.endswith("png"):
                self.link = t_link
                self.img_flag = 1

    def handle_endtag(self, tag):
        if 'html' == tag:
            print("END")
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

class ImgParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.img_rend_flag = 0
        self.link = ""

    def handle_starttag(self, tag, attrs):
        if 'img' == tag:
            ch_img = dict(attrs)["src"]
            if ch_img.endswith("renderTimingPixel.png"):
                self.img_rend_flag = 1

        if 'a' == tag and self.img_rend_flag == 1:
            t_dict = dict(attrs)
            if (t_dict["href"].endswith("png") or t_dict["href"].endswith("jpg")):
                self.link = t_dict["href"]
                self.img_rend_flag = 0

def red_crawler():
    red_url = "https://www.reddit.com"
    categ = "/r/EarthPorn"

    print(f"Trying to fetch {red_url+categ}")
    url_obj = urlopen(Request(red_url+categ, headers=custom_header))
    html_page = str(url_obj.read())

    red_parser_obj = RedditEpParser()
    red_parser_obj.feed(html_page)
    post_link = red_parser_obj.final_link
    if len(post_link) == 0:
        print("No high res image found, exiting")
        with open("test.html",'w') as out_f:
            out_f.write(html_page)
        import sys
        sys.exit()
    print("Obtained the post link ", post_link)

    redimg_parser_obj = ImgParser()
    img_url = red_url + post_link
    print("Trying to fetch ", img_url)
    url_obj = urlopen(Request(img_url, headers = custom_header))
    html_page = str(url_obj.read())

    redimg_parser_obj.feed(html_page)
    img_link = redimg_parser_obj.link
    print("Trying to download ", img_link)
    print(img_link)
    img_link_obj = urlopen(Request(img_link, headers = custom_header))

    img_name = "todays_image.jpg"# + img_link.split('/')[-1]
    with open(img_name, "wb") as img_file:
        img_file.write(img_link_obj.read())
    print("Image Downloaded successfully")
    return img_name

def main():
    red_crawler()

if __name__ == "__main__":
    main()
