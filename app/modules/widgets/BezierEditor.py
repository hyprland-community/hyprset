from ..imports import Gtk, Gdk, Adw, GObject, Bezier, Tuple, Union
from ..utils import fg_color, accent_color
from dataclasses import dataclass
import math


@dataclass
class Point:
    x: Union[int, float]
    y: Union[int, float]


class BezierEditor(Gtk.DrawingArea):
    __gsignals__ = {
        'changed': (GObject.SignalFlags.RUN_FIRST, None, ()),
    }

    def __init__(self):
        super().__init__()
        self.add_css_class('bezier-editor')
        self.set_size_request(400, 400)
        self.set_halign(Gtk.Align.CENTER)
        self._entry_row = None

        self.points = [Point(150, 300), Point(250, 100)]
        self.initial_positions = [(50, 350), (350, 50)]
        self.dragging = None

        self.controller = Gtk.EventControllerLegacy.new()
        self.controller.connect('event', self.on_event)
        self.add_controller(self.controller)
        self.set_draw_func(self.do_draw)

    def do_draw(self, _, cr, *__):
        grid_size = 20
        for x in range(50, 350, grid_size):
            cr.move_to(x, 50)
            cr.line_to(x, 350)
        for y in range(50, 350, grid_size):
            cr.move_to(50, y)
            cr.line_to(350, y)

        cr.set_source_rgba(
            fg_color.red, fg_color.green, fg_color.blue, 0.1  # type: ignore
        )
        cr.set_line_width(1)
        cr.stroke()

        # Diagonal Line
        cr.move_to(50, 350)
        cr.line_to(350, 50)
        cr.set_line_width(2)
        cr.stroke()

        # Dots
        cr.set_source_rgba(
            fg_color.red, fg_color.green, fg_color.blue, 0.8  # type: ignore
        )
        cr.set_line_width(3)
        for initial, point in zip(self.initial_positions, self.points):
            cr.move_to(initial[0], initial[1])
            cr.line_to(point.x, point.y)
            cr.stroke()

        # Bezier
        cr.set_line_width(4)
        cr.move_to(50, 350)
        cr.curve_to(
            self.points[0].x,
            self.points[0].y,
            self.points[1].x,
            self.points[1].y,
            350,
            50,
        )
        cr.set_source_rgba(
            accent_color.red, accent_color.green, accent_color.blue, 1  # type: ignore
        )
        cr.set_line_width(3)
        cr.stroke()

        # Square
        cr.rectangle(50, 50, 300, 300)
        cr.set_source_rgba(
            fg_color.red, fg_color.green, fg_color.blue, 0.1  # type: ignore
        )
        cr.set_line_width(3)
        cr.stroke()

        # Dots
        for point in self.points:
            cr.arc(point.x, point.y, 10, 0, 2 * math.pi)
            cr.set_source_rgba(
                fg_color.red, fg_color.green, fg_color.blue, 1  # type: ignore
            )
            cr.fill()

    def on_event(self, newEvent: Gtk.EventControllerLegacy, _) -> None:
        Event: Gdk.Event = Gtk.EventController.get_current_event(newEvent)

        match type(Event):
            case Gdk.MotionEvent:
                self.on_motion_notify(Event)   # type: ignore

            case Gdk.ButtonEvent:

                button: int = Event.get_button()   # type:ignore
                state: Gdk.ModifierType = Event.get_modifier_state()
                if button != 1:
                    return
                if state != Gdk.ModifierType.BUTTON1_MASK:
                    self.on_button_press(Event)
                elif state != Gdk.ModifierType.NO_MODIFIER_MASK:
                    self.on_button_release(Event)
            case Gdk.TouchpadEvent:
                pass
            case Gdk.ScrollEvent:
                pass
            case _:
                print(Event, type(Event))
                pass

    def on_button_release(self, _):
        self.dragging = None

    def on_button_press(self, event: Gdk.Event):
        x, y = self.get_eventpos(event)

        for i, point in enumerate(self.points):
            if (x - point.x) ** 2 + (y - point.y) ** 2 <= 10**2:
                self.dragging = i
                break

    def on_motion_notify(self, event: Gdk.MotionEvent):
        if self.dragging is not None:
            x = min(max(self.get_eventpos(event)[0], 50), 350)   # type: ignore
            y = self.get_eventpos(event)[1]   # type: ignore

            self.points[self.dragging].x = x
            self.points[self.dragging].y = y

            self.emit('changed')
            self.queue_draw()

    def get_bezier(self) -> Tuple[float, float, float, float]:
        x0 = (self.points[0].x - 50) / 300
        y0 = 1 - (self.points[0].y - 50) / 300
        x1 = (self.points[1].x - 50) / 300
        y1 = 1 - (self.points[1].y - 50) / 300
        return (x0, y0, x1, y1)

    def set_bezier(self, x0: float, y0: float, x1: float, y1: float) -> None:
        self.points[0].x = x0 * 300 + 50
        self.points[0].y = (1 - y0) * 300 + 50
        self.points[1].x = x1 * 300 + 50
        self.points[1].y = (1 - y1) * 300 + 50
        return self.queue_draw()

    def get_eventpos(self, event) -> Tuple[float, float]:
        _, x, y = event.get_position()
        return x - 20, y - 45


class BezierEditorWindow(Adw.Window):
    __gsignals__ = {
        'bezier-updated': (GObject.SignalFlags.RUN_FIRST, None, ()),
    }

    def __init__(self) -> None:
        super().__init__()
        self.editing: Bezier

        self.set_size_request(400, 700)
        self.set_modal(True)
        self.set_hide_on_close(True)
        self.set_resizable(False)
        self.set_destroy_with_parent(True)

        self.root = Adw.ToolbarView.new()
        self.top_bar = Adw.HeaderBar.new()
        self.top_bar.set_title_widget(
            Adw.WindowTitle.new('Bezier Settings', '')
        )

        self.bezier_editor = BezierEditor()
        self.bezier_editor.connect('changed', self.on_editor_changed)
        self.preferences_group = Adw.PreferencesGroup.new()
        self.box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.box.add_css_class('bezier-editor-container')
        self.update_graph = True

        self.entry_x0 = Adw.EntryRow.new()
        self.entry_y0 = Adw.EntryRow.new()
        self.entry_x1 = Adw.EntryRow.new()
        self.entry_y1 = Adw.EntryRow.new()
        self.entry_x0.set_title('X0')
        self.entry_y0.set_title('Y0')
        self.entry_x1.set_title('X1')
        self.entry_y1.set_title('Y1')

        self.set_content(self.root)
        self.root.add_top_bar(self.top_bar)
        self.root.set_content(self.box)
        self.box.append(self.bezier_editor)
        self.box.append(self.preferences_group)

        for i in [self.entry_x0, self.entry_y0, self.entry_x1, self.entry_y1]:
            i.connect('changed', self.on_changed)
            self.preferences_group.add(i)

    def on_changed(self, _: Gtk.Entry) -> None:
        if not self.update_graph:
            return
        try:
            tmp = []
            for i, entry in enumerate(
                [
                    self.entry_x0,
                    self.entry_y0,
                    self.entry_x1,
                    self.entry_y1,
                ]
            ):
                tmp += [float(entry.get_text())]  # type: ignore
                if tmp[i] > 2:
                    tmp[i] = 1
            self.bezier_editor.set_bezier(*tmp)
        except ValueError:
            pass
        except Exception as e:
            print(e)

    def on_editor_changed(self, _: BezierEditor) -> None:
        newValues = self.bezier_editor.get_bezier()
        newValues = tuple(round(i, 3) for i in newValues)

        self.update_graph = False
        self.entry_x0.set_text(f'{newValues[0]}')
        self.entry_y0.set_text(f'{newValues[1]}')
        self.entry_x1.set_text(f'{newValues[2]}')
        self.entry_y1.set_text(f'{newValues[3]}')
        self.update_graph = True

    def on_click(self, _: Gtk.Button) -> None:
        pass

    def edit_bezier(self, bezier: Bezier) -> None:
        self.editing = bezier
        self.bezier_editor.set_bezier(*self.editing.transition)
        self.bezier_editor.emit('changed')

        return self.present()


MyBezierEditorWindow = BezierEditorWindow()
