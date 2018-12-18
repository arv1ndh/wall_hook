import dbus
import os

def change_wall():

    if not os.path.isfile("resized_img.jpg"):
        print("Resized file not available")
        return
    os.rename("resized_img.jpg", "final_wall_img.jpg")

    p_command = """
    var allDesktops = desktops();
    for (i=0;i<allDesktops.length;i++) {
        d = allDesktops[i];
        d.wallpaperPlugin = "org.kde.image";
        d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
        d.writeConfig("Image", "file:///home/arvindh/my_git/wall_hook/final_wall_img.jpg")
    }
    """
    bus = dbus.SessionBus()
    plasma = dbus.Interface(bus.get_object('org.kde.plasmashell','/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
    plasma.evaluateScript(p_command)

#if __name__ == "__main__":
#    main()
