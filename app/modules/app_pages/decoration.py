import gi

gi.require_version("Adw", "1")
from gi.repository import Adw

decoration_page = Adw.PreferencesPage.new()

general_page_windows_settings = Adw.PreferencesGroup.new()
general_page_windows_settings.set_title("Windows")
general_page_windows_settings.set_description(
    "Adjust windows's borders, padding, etc..."
)

decoration_page.add(general_page_windows_settings)
