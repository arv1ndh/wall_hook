from PIL import Image
import os

def image_resizer():
    if not os.path.isfile("todays_img.jpg"):
        print("Image not present")
        return
    print("Opening todays_img.jpg")
    img_obj = Image.open("todays_img.jpg", "r")
    img_obj = img_obj.resize((1920,1080))
    img_obj.save("resized_img.jpg")
    print("Image resized successfully")
    


#if __name__ == "__main__":
#    main()
