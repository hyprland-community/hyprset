from ..imports import Adw


class ExpanderRow(Adw.ExpanderRow):
    def __init__(self, title: str, subtitle: str) -> None:
        super().__init__()
        self.set_title(title)
        self.set_subtitle(subtitle)
