from ..imports import Adw
from .Icon import Icon


class ButtonRow(Adw.ActionRow):
    def __init__(
        self,
        prefix: str,
        title: str,
        subtitle: str,
        on_activated=lambda self: self,
    ) -> None:
        super().__init__()
        self.set_title(title)
        self.set_subtitle(subtitle)
        self.set_activatable(True)
        self.add_prefix(Icon(prefix))
        self.add_suffix(Icon('go-next-symbolic'))
        self.connect('activated', on_activated)
