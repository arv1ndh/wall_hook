from red_crawler import red_crawler
from image_resizer import image_resizer
from change_wall import change_wall

def main():
    img_name = red_crawler()
    resize_img_name = image_resizer(img_name)
    change_wall(resize_img_name)

if __name__ == "__main__":
    main()
