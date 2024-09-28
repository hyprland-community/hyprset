from ..imports import Adw


class PreferencesGroup(Adw.PreferencesGroup):
    def __init__(self, title: str, description: str):
        super().__init__()
        self.set_title(title)
        self.set_description(description)
