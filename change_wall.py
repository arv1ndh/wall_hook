import dbus

def main():
    p_command = """
    var allDesktops = desktops();
    for (i=0;i<allDesktops.length;i++) {
        d = allDesktops[i];
        d.wallpaperPlugin = "org.kde.image";
        d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
        d.writeConfig("Image", "file:///home/arvindh/my_git/wall_hook/resized_img.jpg")
    }
    """
    bus = dbus.SessionBus()
    plasma = dbus.Interface(bus.get_object('org.kde.plasmashell','/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
    plasma.evaluateScript(p_command)

if __name__ == "__main__":
    main()
