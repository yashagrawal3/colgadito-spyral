from gettext import gettext as _
import gtk
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

        self._pygamecanvas = sugargame2.canvas.PygameCanvas(self)
        self._pygamecanvas.set_flags(gtk.EXPAND)
        self._pygamecanvas.set_flags(gtk.FILL)
        self.box.append_page(self._pygamecanvas)
       
        self.box.show()
        self.set_canvas(self.box)

        def run():
            import game
            spyral.director.init((0,0), fullscreen=False, max_fps=30)
            game.main(self)
            spyral.director.run(sugar = True)

        self.build_toolbar()    
        self._pygamecanvas.run_pygame(run)

    def build_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

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
