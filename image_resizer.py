from PIL import Image
import os

def image_resizer(image_name):
    if not os.path.isfile(image_name):
        print("Image not present")
        return
    print("Opening todays_img.jpg")
    img_obj = Image.open("todays_img.jpg", "r")
    img_obj = img_obj.resize((1920,1080))
    resize_img_name = "resized_" + image_name.split('_')[1]
    img_obj.save(resize_img_name)
    print("Image resized successfully")
    os.remove(image_name)
    return resize_img_name
    


#if __name__ == "__main__":
#    main()
