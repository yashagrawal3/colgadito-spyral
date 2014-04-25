from gettext import gettext as _
import gtk
import gobject
import pygame
import sugar.activity.activity
import libraries
libraries.setup_path()
import sugargame2
import sugargame2.canvas
import spyral

from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityToolbarButton
from sugar.graphics.toolbutton import ToolButton
from sugar.activity.widgets import StopButton

from terminal.interactiveconsole import GTKInterpreterConsole

from game.colgadito_gui import Game

class Activity(sugar.activity.activity.Activity):
    def __init__(self, handle):
        super(Activity, self).__init__(handle)
        self.paused = False
        
        self.box = gtk.Notebook()
        self.box.set_show_tabs(False)

        self.splash = gtk.Image()
        self.splash.set_from_file("images/splash.png")
        self.splash.show()
        eb = gtk.EventBox()
        eb.add(self.splash)
        eb.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
        eb.show()
        self.box.append_page(eb)

        watch = gtk.gdk.Cursor(gtk.gdk.WATCH)
        self.window.set_cursor(watch)

        self.p = gtk.VPaned()
        self._pygamecanvas = sugargame2.canvas.PygameCanvas(self)
        self._pygamecanvas.set_flags(gtk.EXPAND)
        self._pygamecanvas.set_flags(gtk.FILL)
        self.p.pack2(self._pygamecanvas)
       
        self.p.connect("notify::position", self.redraw)
        self.connect("visibility-notify-event", self.redraw)
        self._pygamecanvas.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        self._pygamecanvas.connect("button-press-event", self._pygamecanvas.grab_focus)

        self.p.show()
        self.box.append_page(self.p)
        self.box.show()
        self.set_canvas(self.box)

        gobject.timeout_add(2000, self.pump)
        gobject.timeout_add(2000, self.init_interpreter)

        self.build_toolbar()    
        self._pygamecanvas.run_pygame(self.run_game)

    def redraw(self, a=None, b=None):
        scene = spyral.director.get_scene()
        if scene:
            scene.redraw()

    def pump(self):
        pygame.event.pump()

    def focus_interpreter(self, widget, event):
        self._interpreter.text.grab_focus()
        return True

    def init_interpreter(self):
        # diferido  unos segundos para evitar ver errores superfluos
        self._interpreter = GTKInterpreterConsole(self.redraw)
        self._interpreter.text.connect('button-press-event', self.focus_interpreter)
        self.p.pack1(self._interpreter)
        return False

    def run_game(self):
        spyral.director.init((0,0), fullscreen=False, max_fps=30)
        self.game = Game(self)

        spyral.director.push(self.game)
        spyral.director.run(sugar = True)

    def build_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        button = ToolButton('tray-favourite')
        button.set_tooltip(_('Interprete'))
        button.connect('clicked', self.toggle_console)
        toolbar_box.toolbar.insert(button, -1)
        button.show()

        # Blank space (separator) and Stop button at the end:

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

    def read_file(self, file_path):
        pass

    def write_file(self, file_path):
        pass

    def can_close(self):
        self.box.prev_page()
        pygame.quit()
        return True

    def toggle_console(self, e):
        if self._interpreter.props.visible:
            self._interpreter.hide()
            self._pygamecanvas.grab_focus()
        else:
            self.p.set_position(160)
            self._interpreter.show()
            self._interpreter.text.grab_focus()
        self.redraw()

def main():
    spyral.director.init((0,0), fullscreen = False, max_fps = 30)
    import game
    game.main()
    try:
        spyral.director.run()
    except KeyboardInterrupt:
        pygame.quit()

if __name__ == '__main__':
    main()
