from modules.app_pages import PAGES_DICT, PAGES_LIST
from modules.imports import Adw, Gdk, Gio, GLib, Gtk
from modules.structures import ToastOverlay


class ApplicationWindow(Adw.ApplicationWindow):
    def __init__(self, app: Adw.Application):
        super().__init__(application=app)
        self.set_default_size(800, 600)
        self.root = Adw.NavigationSplitView.new()
        self.set_content(self.root)

        # Main Content
        self.main_content = Adw.ToolbarView.new()
        self.main_content_navigation_page = Adw.NavigationPage.new(
            self.main_content, "General"
        )
        self.main_content_top_bar = Adw.HeaderBar.new()
        self.main_content_top_bar_title = Adw.WindowTitle.new(
            "General", "Gaps, borders, colors, cursor and other settings."
        )

        self.main_content.add_top_bar(self.main_content_top_bar)
        self.main_content_top_bar.set_title_widget(self.main_content_top_bar_title)
        self.main_content_view_stack = Adw.ViewStack.new()

        self.toast_overlay = ToastOverlay
        self.toast_overlay.instance.set_child(self.main_content_view_stack)
        self.main_content.set_content(self.toast_overlay.instance)

        # Sidebar
        self.sidebar = Adw.ToolbarView()
        self.sidebar.add_css_class("list-box-scroll")
        self.sidebar_navigation_page = Adw.NavigationPage.new(self.sidebar, "Settings")
        self.sidebar_navigation_page.add_css_class("sidebar")
        self.sidebar_top_bar = Adw.HeaderBar.new()
        self.sidebar.add_top_bar(self.sidebar_top_bar)
        self.sidebar_scrolled_window = Gtk.ScrolledWindow.new()
        self.sidebar_listbox = Gtk.ListBox.new()
        self.sidebar_scrolled_window.set_child(self.sidebar_listbox)
        self.sidebar.set_content(self.sidebar_scrolled_window)

        for item in PAGES_LIST:
            if item.get("separator"):
                tmp_rowbox = Gtk.ListBoxRow.new()
                tmp_rowbox.set_child(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL))
                tmp_rowbox.set_can_focus(False)
                tmp_rowbox.set_activatable(False)
                tmp_rowbox.set_selectable(False)
                tmp_rowbox.set_sensitive(False)

            else:
                tmp_grid = Gtk.Grid.new()
                tmp_grid.set_column_spacing(12)
                tmp_grid.set_valign(Gtk.Align.CENTER)
                tmp_grid.set_vexpand(True)

                tmp_rowbox = Gtk.ListBoxRow.new()
                tmp_rowbox.add_css_class("list-box-row")
                setattr(tmp_rowbox, "title", item["label"])
                setattr(tmp_rowbox, "desc", item["desc"])

                tmp_filepath = "{}/icons/{}.svg".format(__file__[:-12], item["icon"])
                if GLib.file_test(tmp_filepath, GLib.FileTest.EXISTS):
                    icon = Gtk.Image.new_from_gicon(
                        Gio.FileIcon.new(Gio.File.new_for_path(tmp_filepath))
                    )
                else:
                    icon = Gtk.Image.new_from_icon_name(item["icon"])

                label = Gtk.Label.new(item["label"])
                tmp_grid.attach(icon, 0, 0, 1, 1)
                tmp_grid.attach(label, 1, 0, 1, 1)
                tmp_rowbox.set_child(tmp_grid)

            self.sidebar_listbox.insert(tmp_rowbox, -1)

        self.sidebar_listbox.connect("row-activated", self.on_row_activated)
        self.root.set_sidebar(self.sidebar_navigation_page)
        self.root.set_content(self.main_content_navigation_page)

        shortcut_controller = Gtk.ShortcutController.new()
        # Add ctrl+s shortcut
        shortcut_controller.add_shortcut(
            Gtk.Shortcut.new(
                Gtk.ShortcutTrigger.parse_string("<Control>s"),
                Gtk.CallbackAction.new(self.toast_overlay.save_changes),
            )
        )

        self.root.add_controller(shortcut_controller)
        self.present()
        self.sidebar_listbox.unselect_all()
        return self.add_pages()

    def on_row_activated(self, _, sidebar_rowbox: Gtk.ListBoxRow):
        self.main_content_top_bar_title.set_title(getattr(sidebar_rowbox, "title"))
        self.main_content_top_bar_title.set_subtitle(getattr(sidebar_rowbox, "desc"))
        self.main_content_view_stack.set_visible_child_name(
            getattr(sidebar_rowbox, "title")
        )

    def add_pages(self):
        for name, page in PAGES_DICT.items():
            self.main_content_view_stack.add_named(
                page,
                name,
            )


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__()
        self.window = None
        self.set_application_id("com.tokyob0t.HyprSettings")
        self.set_flags(Gio.ApplicationFlags.FLAGS_NONE)
        self.load_css()

    def load_css(self) -> None:

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(f"{__file__[:-12]}/style.css")

        return Gtk.StyleContext.add_provider_for_display(  # type: ignore
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def do_activate(self) -> None:
        if not self.window:
            self.window = ApplicationWindow(self)
        return self.window.present()


if __name__ == "__main__":
    try:
        app = Application()
        app.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        exit(0)
