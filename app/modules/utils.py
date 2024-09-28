from .imports import Gdk, Literal, Tuple, Gtk
import string


string.ascii_lowercase = string.ascii_lowercase + ' '

# Im so fukin dumb, didnt know that Gdk.RGBA had Gdk.RGBA.parse() function


class ParseColor:
    @staticmethod
    def rgba_str_to_hex(color: str) -> str:
        color = (
            ParseColor.format_rgba(color).replace('rgba(', '').replace(')', '')
        )
        rgba = list(map(int, color.split(',')))

        r, g, b = rgba[:3]
        a = rgba[3] if len(rgba) == 4 else 255

        return f'#{r:02X}{g:02X}{b:02X}{a:02X}'

    @staticmethod
    def rgba_float_to_hex(color: Tuple[float, float, float, float]) -> str:
        r = int(color[0] * 255.0)
        g = int(color[1] * 255.0)
        b = int(color[2] * 255.0)
        a = int(color[3] * 255.0)

        return f'#{r:02X}{g:02X}{b:02X}{a:02X}'

    @staticmethod
    def hex_to_rgba_float(color: str) -> Tuple[float, float, float, float]:
        color = ParseColor.format_hex(color)
        r = int(color[1:3], 16) / 255.0
        g = int(color[3:5], 16) / 255.0
        b = int(color[5:7], 16) / 255.0
        a = (int(color[7:9], 16) / 255.0) if len(color) == 8 else 1.0
        return (r, g, b, a)

    @staticmethod
    def hex_to_rgba_str(color: str) -> str:
        color = ParseColor.format_hex(color)

        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        a = int(color[7:9], 16) / 255

        return f'rgba({r},{g},{b},{a:.2f})'

    @staticmethod
    def hex_to_gdk_rgba(color: str) -> Gdk.RGBA:
        color = ParseColor.format_hex(color)
        r = int(color[1:3], 16) / 255.0
        g = int(color[3:5], 16) / 255.0
        b = int(color[5:7], 16) / 255.0
        a = int(color[7:9], 16) / 255.0 if len(color) == 9 else 1.0
        return Gdk.RGBA(r, g, b, a)   # type:ignore

    @staticmethod
    def gdk_rgba_to_hex(color: Gdk.RGBA) -> str:
        r = int(color.red * 255)   # type: ignore
        g = int(color.green * 255)   # type:ignore
        b = int(color.blue * 255)   # type:ignore
        a = int(color.alpha * 255)   # type:ignore
        return f'#{r:02X}{g:02X}{b:02X}{a:02X}'

    @staticmethod
    def format_hex(text: str) -> str:
        color = text.strip().lower().replace('#', '')
        color = ''.join(i if i in '1234567890abcdef' else 'f' for i in color)

        if len(text) < 6:
            color = f'{color:0<6}'

        if len(text) < 8:
            color = f'{color:f<8}'

        if len(text) > 8:
            color = color[:8]

        return '#{}'.format(color)

    @staticmethod
    def format_rgba(text: str) -> str:
        color = (
            text.strip()
            .lower()
            .replace('rgba', '')
            .replace('rgb', '')
            .strip('()')
        )

        color = ''.join(
            i if i in '1234567890,' else '0'
            for i in color
            if i not in string.ascii_lowercase
        )

        sections = color.split(',')
        sections = [s.ljust(3, '0')[:3] for s in sections]

        if len(sections) < 3:
            sections.extend(['0'] * (3 - len(sections)))

        if len(sections) == 3:
            if text.strip().startswith('rgba'):
                sections.append('0')
            elif text.strip().startswith('rgb'):
                sections.append('255')

        return 'rgba({})'.format(','.join(sections))

    @staticmethod
    def is_color(text: str) -> bool:
        text = text.strip().lower()
        if text.startswith('rgb'):
            return True
        elif text.startswith('#'):
            return True
        return False

    @staticmethod
    def color_type(text: str) -> Literal['rgba', 'hex', None]:
        text = text.strip().lower()
        if text.startswith('rgb'):
            return 'rgba'
        elif text.startswith('#'):
            return 'hex'
        return None


# idk how else obtain a gtk theme var, so

tmp = Gtk.Box()
tmp.add_css_class('custom-box')

ctx = tmp.get_style_context()

provider = Gtk.CssProvider.new()

provider.load_from_data('.custom-box {color: @accent_color; }')
ctx.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
accent_color: Gdk.RGBA = ctx.get_color()   # type: ignore

provider.load_from_data('.custom-box {color: @card_bg_color; }')
ctx.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
bg_color: Gdk.RGBA = ctx.get_color()   # type: ignore

provider.load_from_data('.custom-box {color: @card_fg_color; }')
ctx.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
fg_color: Gdk.RGBA = ctx.get_color()   # type: ignore
