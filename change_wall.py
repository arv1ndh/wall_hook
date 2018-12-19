import dbus
import os

def change_wall(image_file_name):

    if not os.path.isfile(image_file_name):
        print("Resized file not available")
        return
    old_file = ""
    try:
        old_file = list(filter(lambda x:x.startswith("final_"), [img_f for img_f in os.listdir(".")]))[0]
    except IndexError:
        pass
    if len(old_file):
        os.remove(old_file)
        print("Removed old file ", old_file)
    final_image_name = "final_" + image_file_name.split('_')[1]
    os.rename(image_file_name, final_image_name)

    p_command = """
    var allDesktops = desktops();
    for (i=0;i<allDesktops.length;i++) {
        d = allDesktops[i];
        d.wallpaperPlugin = "org.kde.image";
        d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
        d.writeConfig("Image", "file:///home/arvindh/my_git/wall_hook/%s")
    }
    """
    bus = dbus.SessionBus()
    plasma = dbus.Interface(bus.get_object('org.kde.plasmashell','/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
    #print(p_command % final_image_name)
    plasma.evaluateScript(p_command % final_image_name)

#def main():
#    change_wall("r_sxf5.jpg")
#
#if __name__ == "__main__":
#    main()
