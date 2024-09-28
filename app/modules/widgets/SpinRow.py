from types import new_class
from ..imports import Gtk, Union, Type, Adw, Setting, HyprData
from .CustomToastOverlay import ToastOverlay


def Adjustment(
    section: Union[str, None],
    data_type: Type[Union[int, float]] = int,
    min: Union[int, float] = 0,
    max: Union[int, float] = 255,
):
    new_adjustment = Gtk.Adjustment(lower=min, upper=max, page_size=0)

    new_adjustment.data_type = data_type
    new_adjustment.section = section

    if data_type.__name__ == "int":
        new_adjustment.set_step_increment(1)
        new_adjustment.set_page_increment(10)
    else:
        new_adjustment.set_step_increment(0.1)
        new_adjustment.set_page_increment(1.0)

    ToastOverlay.instances.append(new_adjustment)

    if new_adjustment.section is not None:
        opt = HyprData.get_option(new_adjustment.section)

        if not opt:
            opt = Setting(new_adjustment.section, 1)
            HyprData.new_option(opt)

        if isinstance(opt.value, (int, float)):
            new_adjustment.set_value(opt.value)

        new_adjustment._default = (opt.value, False)
    else:
        new_adjustment._default = (0, False)

    def update_default(*args, **kwargs) -> None:
        new_adjustment._default = (new_adjustment.get_value(), False)

    def on_value_changed(self):
        if new_adjustment._default[0] != new_adjustment.get_value():
            if not new_adjustment._default[1]:
                ToastOverlay.add_change()
                new_adjustment._default = (new_adjustment._default[0], True)
        else:
            ToastOverlay.del_change()
            new_adjustment._default = (self._default[0], False)

        if new_adjustment.section is None:
            return

        if self.data_type.__name__ == "int":
            return HyprData.set_option(
                new_adjustment.section, round(new_adjustment.get_value())
            )
        return HyprData.set_option(new_adjustment.section, new_adjustment.get_value())

    new_adjustment.update_default = update_default
    new_adjustment.connect("value-changed", on_value_changed)

    return new_adjustment


def SpinRow(
    title: str,
    subtitle: str,
    section: str,
    data_type: Type[Union[int, float]] = int,
    min: Union[int, float] = 0,
    max: Union[int, float] = 255,
    decimal_digits: int = 2,
):
    new_spinrow = Adw.SpinRow(adjustment=Adjustment(section, data_type, min, max),title=title,
    subtitle=subtitle
    )


    if data_type.__name__ == "float":
        new_spinrow.set_digits(decimal_digits)

    return new_spinrow


class _Adjustment(Gtk.Adjustment):
    def __init__(
        self,
        section: Union[str, None],
        data_type: Type[Union[int, float]] = int,
        min: Union[int, float] = 0,
        max: Union[int, float] = 255,
    ):
        super().__init__()
        self.data_type = data_type
        self.set_lower(min)
        self.set_upper(max)
        self.set_page_size(0)

        if data_type.__name__ == "int":
            self.set_step_increment(1)
            self.set_page_increment(10)
        else:
            self.set_step_increment(0.1)
            self.set_page_increment(1.0)

        ToastOverlay.instances.append(self)

        self.section = section

        if self.section is not None:
            opt = HyprData.get_option(self.section)

            if not opt:
                opt = Setting(self.section, 1)
                HyprData.new_option(opt)

            if isinstance(opt.value, (int, float)):
                self.set_value(opt.value)

            self._default = (opt.value, False)
        else:
            self._default = (0, False)

        self.connect("value-changed", self.on_value_changed)

    def on_value_changed(self, _):
        if self._default[0] != self.get_value():
            if not self._default[1]:
                ToastOverlay.add_change()
                self._default = (self._default[0], True)
        else:
            ToastOverlay.del_change()
            self._default = (self._default[0], False)

        if self.section is None:
            return

        if self.data_type.__name__ == "int":
            return HyprData.set_option(self.section, round(self.get_value()))
        return HyprData.set_option(self.section, self.get_value())

    def update_default(self) -> None:
        self._default = (self.get_value(), False)


class _SpinRow:
    def __init__(
        self,
        title: str,
        subtitle: str,
        section: str,
        data_type: Type[Union[int, float]] = int,
        min: Union[int, float] = 0,
        max: Union[int, float] = 255,
        decimal_digits: int = 2,
    ):
        self._instance = Adw.SpinRow()
        self.instance.set_adjustment(Adjustment(section, data_type, min, max))
        self.instance.set_title(title)
        self.instance.set_subtitle(subtitle)

        if data_type.__name__ == "float":
            self.instance.set_digits(decimal_digits)

    @property
    def instance(self) -> Adw.SpinRow:
        return self._instance
