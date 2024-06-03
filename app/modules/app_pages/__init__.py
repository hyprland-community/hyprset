from .decoration import decoration_page
from .general import general_page

PAGES_DICT = {
    "General": general_page,
    "Decoration": decoration_page,
}

PAGES_LIST = [
    {
        "icon": "settings-symbolic",
        "label": "General",
        "desc": "Gaps, borders, colors, cursor and other settings.",
    },
    {
        "icon": "window-new-symbolic",
        "label": "Decoration",
        "desc": "Rounding, blur, shadow, dim...",
    },
    {
        "icon": "graph-symbolic",
        "label": "Animations",
        "desc": "Change animations settings.",
    },
    {"separator": True},
    {
        "icon": "input-keyboard-symbolic",
        "label": "Input",
        "desc": "Change input settings.",
    },
    {
        "icon": "input-touchpad-symbolic",
        "label": "Gestures",
        "desc": "Gesture and swipe settings.",
    },
    {
        "icon": "overlapping-windows-symbolic",
        "label": "Group",
        "desc": "Change group settings.",
    },
    {"separator": True},
    {
        "icon": "preferences-system-symbolic",
        "label": "Misc",
        "desc": "Change miscellaneous settings.",
    },
    {
        "icon": "preferences-desktop-keyboard-shortcuts-symbolic",
        "label": "Binds",
        "desc": "Change binds settings.",
    },
    {
        "icon": "shapes-symbolic",
        "label": "Variables",
        "desc": "Adjust variables.",
    },
    {"separator": True},
    {
        "icon": "preferences-desktop-theme-symbolic",
        "label": "Wallpaper",
        "desc": "Hyprpaper settings.",
    },
    {"icon": "bed-symbolic", "label": "Idle", "desc": "Hypridle settings."},
    {
        "icon": "system-lock-screen-symbolic",
        "label": "Lock",
        "desc": "Hyprlock settings.",
    },
    {"separator": True},
    {"icon": "view-more-symbolic", "label": "More", "desc": ""},
]
