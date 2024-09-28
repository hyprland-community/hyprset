from ..imports import Literal, Gio, GLib, Gtk


def Icon(
    name: str, size: Literal["large", "normal", "inherit"] = "normal"
) -> Gtk.Image:
    new_icon = Gtk.Image.new()
    new_icon.filepath = "{}/icons/{}.svg".format(__file__[:-24], name)

    if GLib.file_test(new_icon.filepath, GLib.FileTest.EXISTS):
        new_icon.set_from_gicon(
            Gio.FileIcon.new(Gio.File.new_for_path(new_icon.filepath))
        )
    else:
        new_icon.set_from_icon_name(name)
    match size:
        case "large":
            new_icon.set_icon_size(Gtk.IconSize.LARGE)
        case "normal":
            new_icon.set_icon_size(Gtk.IconSize.NORMAL)
        case "inherit":
            new_icon.set_icon_size(Gtk.IconSize.INHERIT)

    return new_icon
