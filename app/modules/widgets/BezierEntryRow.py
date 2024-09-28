from ..imports import Adw, Gtk, Bezier, HyprData, Tuple, string, GObject, Gdk
from .BezierEditor import MyBezierEditorWindow
from .PreferencesGroup import PreferencesGroup


class NewBezierDialog(Adw.Dialog):
    __gsignals__ = {
        'new-bezier': (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str, float, float, float, float),
        ),
    }

    def __init__(self) -> None:
        super().__init__()

        self.set_title('New Curve')
        self.set_size_request(400, 200)

        self.root = Adw.ToolbarView.new()

        self.top_bar = Adw.HeaderBar.new()
        self.top_bar.set_title_widget(Adw.WindowTitle.new('New Bezier', ''))

        self.body = Adw.PreferencesPage.new()
        self.content = PreferencesGroup('', '')
        self.entry = Adw.EntryRow.new()
        self.entry.set_title('Name')
        self.entry.set_text('Epic_Bezier_Name')
        self.bezier_entry = Adw.EntryRow.new()
        self.bezier_entry.set_title('Bezier')
        self.bezier_entry.set_text('cubic-bezier(0.25, 0.75, 0.75, 0.25)')

        self.button = Gtk.Button.new()
        self.button.set_label('Add Bezier')
        self.button.set_halign(Gtk.Align.CENTER)
        self.button.set_hexpand(True)
        self.button.add_css_class('suggested-action')
        self.button.add_css_class('pill')
        self.button.set_margin_top(20)
        self.button.connect('clicked', self.on_activate)

        self.root.add_top_bar(self.top_bar)
        self.root.set_content(self.body)
        self.body.add(self.content)
        self.content.add(self.entry)
        self.content.add(self.bezier_entry)
        self.content.add(self.button)
        self.set_child(self.root)

    def on_activate(self, _) -> None:
        state, bezier = self.parse_bezier(
            self.bezier_entry.get_text()  # type: ignore
        )
        name = self.parse_name(self.entry.get_text())

        if state and name and name not in HyprData.beziers.keys():
            self.emit('new-bezier', name, *bezier)
            self.close()

    def parse_bezier(
        self, bezier: str
    ) -> Tuple[bool, Tuple[float, float, float, float]]:
        bezier = bezier.replace(' ', '').lower()
        if bezier.startswith('cubic-bezier'):
            bezier = bezier[12:]
        bezier = ''.join(
            i for i in bezier if i not in string.ascii_lowercase + '()'
        )
        try:
            x0, y0, x1, y1 = bezier.split(',')
            return (True, tuple(map(float, (x0, y0, x1, y1))))   # type: ignore
        except ValueError:
            pass
        except Exception as e:
            print(e)
        return (False, (0, 0, 0, 0))

    def parse_name(self, text: str) -> str:
        text = text.replace(' ', '')
        text = ''.join(i for i in text if i in string.ascii_letters + '_')
        return text


BezierAddDialog = NewBezierDialog()


class BezierPreviewRow(Adw.ActionRow):
    def __init__(
        self,
        new_bezier: Bezier,
    ) -> None:
        super().__init__()
        self.bezier = new_bezier
        self.edit_button = Gtk.Button.new_from_icon_name(
            'document-edit-symbolic'
        )
        self.del_button = Gtk.Button.new_from_icon_name('user-trash-symbolic')
        self.copy_button = Gtk.Button.new_from_icon_name('edit-copy-symbolic')

        self.set_title(self.bezier.name)
        self.set_subtitle(
            'cubic-bezier({})'.format(
                ', '.join(map(str, self.bezier.transition))
            )
        )

        for i in [
            self.copy_button,
            self.edit_button,
            self.del_button,
        ]:
            i.add_css_class('flat')
            i.set_valign(Gtk.Align.CENTER)
            i.set_focusable(True)
            self.add_suffix(i)


class BezierGroup(PreferencesGroup):
    def __init__(self):
        super().__init__(
            'Curves',
            'Define your own bezier curves.',
        )
        self.children_count = 0

        self.beziers = HyprData.beziers

        self.button = Gtk.Button.new_from_icon_name('list-add-symbolic')
        self.button.add_css_class('flat')
        self.button.set_valign(Gtk.Align.CENTER)
        self.set_header_suffix(self.button)

        for i in self.beziers.values():
            tmp = BezierPreviewRow(i)
            if i.name.lower() == 'linear':
                tmp.del_button.set_sensitive(False)
                tmp.edit_button.set_sensitive(False)

            tmp.del_button.connect('clicked', self.on_clicked_child, tmp)
            tmp.edit_button.connect('clicked', self.on_clicked_child, tmp)
            tmp.copy_button.connect('clicked', self.on_clicked_child, tmp)
            self.add(tmp)

        if 'linear' not in list(map(str.lower, self.beziers.keys())):
            tmp = BezierPreviewRow(Bezier('linear', (0, 0, 1, 1)))
            tmp.del_button.set_sensitive(False)
            tmp.edit_button.set_sensitive(False)
            tmp.del_button.connect('clicked', self.on_clicked_child, tmp)
            tmp.edit_button.connect('clicked', self.on_clicked_child, tmp)
            tmp.copy_button.connect('clicked', self.on_clicked_child, tmp)

        self.button.connect('clicked', self.on_clicked)
        BezierAddDialog.connect('new-bezier', self.on_new_bezier)
        MyBezierEditorWindow.connect('bezier-updated', self.on_updated_bezier)

    def on_clicked(self, _: Gtk.Button) -> None:
        return BezierAddDialog.present(self.get_root())  # type: ignore

    def on_new_bezier(
        self, _, name: str, x0: float, y0: float, x1: float, y1: float
    ) -> None:
        return self.add(BezierPreviewRow(Bezier(name, (x0, y0, x1, y1))))

    def on_updated_bezier(
        self, _, name: str, x0: float, y0: float, x1: float, y1: float
    ):
        pass

    def on_clicked_child(
        self,
        button: Gtk.Button,
        child: BezierPreviewRow,
    ):

        if button is child.del_button:
            return self.remove(child)
        elif button is child.copy_button:
            Gdk.Clipboard.new().set_text('epic')

        elif button is child.edit_button:
            return MyBezierEditorWindow.edit_bezier(child.bezier)

    def add_bezier(self, new_bezier: Bezier) -> None:   # type: ignore
        self.children_count += 1
        return self.add(BezierPreviewRow(new_bezier))

    def update_default(self) -> None:
        pass
