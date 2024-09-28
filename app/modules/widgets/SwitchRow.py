from .CustomToastOverlay import ToastOverlay
from ..imports import Adw, HyprData, Setting


def SwitchRow(title: str, subtitle: str, section: str, *, invert: bool = False):
    new_switchrow = Adw.SwitchRow(title = title, subtitle = subtitle)

    ToastOverlay.instances.append(new_switchrow)
    new_switchrow._invert = invert
    new_switchrow.section = section


    opt = HyprData.get_option(new_switchrow.section)

    if not opt:
        opt = Setting(new_switchrow.section, False)
        HyprData.new_option(opt)

    if new_switchrow._invert:
        new_switchrow.set_active(not opt.value)
    else:
        new_switchrow.set_active(bool(opt.value))

    new_switchrow._default = new_switchrow.get_active()

    def on_active(*args, **kwargs):
        if new_switchrow.get_active() != new_switchrow._default:
            ToastOverlay.add_change()
        else:
            ToastOverlay.del_change()

        if new_switchrow._invert:
            return HyprData.set_option(
                new_switchrow.section, not new_switchrow.get_active()
            )

        return HyprData.set_option(new_switchrow.section, new_switchrow.get_active())

    def update_default(*args, **kwargs):
        new_switchrow._default = new_switchrow.get_active()

    new_switchrow.connect("notify::active", on_active)
    new_switchrow.update_default = update_default
    return new_switchrow


class _SwitchRow:
    def __init__(
        self, title: str, subtitle: str, section: str, *, invert: bool = False
    ) -> None:
        super().__init__()
        ToastOverlay.instances.append(self)
        self.__invert = invert
        self._instance = Adw.SwitchRow()
        self.instance.set_title(title)
        self.instance.set_subtitle(subtitle)
        self.section = section

        opt = HyprData.get_option(self.section)

        if not opt:
            opt = Setting(self.section, False)
            HyprData.new_option(opt)

        if self.__invert:
            self.instance.set_active(not opt.value)
        else:
            self.instance.set_active(bool(opt.value))

        self._default = self.instance.get_active()
        self.instance.connect("notify::active", self.on_activate)

    def on_activate(self, *_):
        if self.instance.get_active() != self._default:
            ToastOverlay.add_change()
        else:
            ToastOverlay.del_change()
        if self.__invert:
            return HyprData.set_option(self.section, not self.instance.get_active())
        return HyprData.set_option(self.section, self.instance.get_active())
