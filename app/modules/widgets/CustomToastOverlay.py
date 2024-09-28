from ..imports import Adw, HyprData


class CustomToastOverlay:
    instances = []

    def __init__(self) -> None:
        self.changes = 0
        self._instance = Adw.ToastOverlay.new()
        self.toast = Adw.Toast.new('You have 0 unsaved changes!')
        self.toast.connect('button-clicked', self.save_changes)
        self.toast.set_button_label('Save now')
        self.toast.set_timeout(0)

    @property
    def instance(self) -> Adw.ToastOverlay:
        return self._instance

    def show_toast(self) -> None:
        self.instance.add_toast(self.toast)

    def hide_toast(self) -> None:
        self.toast.dismiss()

    def add_change(self) -> None:
        self.changes += 1
        self.toast.set_title(f'You have {self.changes} unsaved changes!')
        return self.show_toast()

    def del_change(self) -> None:
        self.changes -= 1
        self.toast.set_title(f'You have {self.changes} unsaved changes!')
        if self.changes == 0:
            return self.hide_toast()

    # After calling this function, each widget updates its new default value.
    def save_changes(self, *_) -> None:
        self.changes = 0
        self.hide_toast()

        for i in CustomToastOverlay.instances:
            i.update_default()
        return HyprData.save_all()


ToastOverlay = CustomToastOverlay()
