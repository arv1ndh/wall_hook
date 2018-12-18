from PIL import Image
import os

def main():
    if not os.path.isfile("todays_img.jpg"):
        print("Image not present")
        return
    img_obj = Image.open("todays_img.jpg", "r")
    img_obj = img_obj.resize((1920,1080))
    img_obj.save("resized_img.jpg")
    


if __name__ == "__main__":
    main()
