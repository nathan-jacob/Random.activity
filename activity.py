# Copyright 2009 Simon Schampijer
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""HelloWorld Activity: A case study for developing an activity."""
import random
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from gettext import gettext as _

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem


class RandomActivity(activity.Activity):
    """HelloWorldActivity class as specified in activity.info"""

    import json
    questions = {}
    questions['Hello'] = 'Hi'
    questions['How are you'] = 'Good'

    # Time Stuff
    import datetime
    import time
    localtime = time.asctime( time.localtime(time.time()) )

    def __init__(self, handle):
        """Set up the HelloWorld activity."""
        activity.Activity.__init__(self, handle)

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1

        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        description_item = DescriptionItem(self)
        toolbar_box.toolbar.insert(description_item, -1)
        description_item.show()

        share_button = ShareButton(self)
        toolbar_box.toolbar.insert(share_button, -1)
        share_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        #make a grid
        self.grid = Gtk.Grid()
        self.set_canvas(self.grid)

        #chat
        self.button2 = Gtk.Button(label="Submit")
        self.button2.connect("clicked", self.chat)
        self.grid.attach(self.button2, 15, 0, 4, 1)
        self.button2.show()

        #entry
        self.entry = Gtk.Entry()
        self.entry.set_width_chars(60)
        self.entry.set_placeholder_text(_("Type in your question or add a question"))
        self.entry.connect("activate", self.chat)
        self.grid.attach(self.entry, 10, 0, 4, 1)
        self.entry.show()

        #Help
        alignment = Gtk.Alignment.new(0., 0.5, 0., 0.)
        self.help_label = Gtk.Label()
        alignment.add(self.help_label)
        help_message = '%s\n%s\n%s\n%s\n%s\n' % (
            _("here are some example questions"),
            _("Pick a number from X to XX"),
            _("Roll a die or a dreidel"),
            _("flip a coin"),
            _("rock, paper, scissors"))
        self.help_label.set_text(help_message)
        self.help_label.show()
        self.grid.attach(alignment, 0, 1, 4, 5)
        alignment.show()
        self.grid.show()

        self.label = Gtk.Label("")
        self.grid.attach(self.label, 0, 0, 4, 1)

    def chat(self, EntryValue):
        query = str(self.entry.get_text()).lower()
        r_value = "unrecognized command"
        i = 0
        if "die" in query:
            r_value = str(random.randint(1,7))
            i = 1
        if "pick a number from " in query:
            query = query.replace("pick a number from ", "")
            query = query.split(" to ")
            r_value = str(random.randint(int(query[0]), int(query[1])))
            i = 1
        if "pick a random number from " in query:
            query = query.replace("pick a random number from ", "")
            query = query.split(" to ")
            r_value = str(random.randint(int(query[0]), int(query[1])))
            i = 1
        if "rock" in query:
            bobby = ["Rock", "Paper", "Scissors"]
            r_value = bobby[random.randint(0,2)]
            i = 1
        if "coin" in query:
            bobby = ["Heads", "Tails"]
            r_value = bobby[random.randint(0,1)]
            i = 1
        if "dreidel" in query:
            bobby = ["Nun", "Gimel", "Hei", "Shin"]
            r_value = bobby[random.randint(0,3)]
            i = 1
        self.label.set_text(r_value)
        if (i == 5):
            self.label.hide()
            self.label.set_text(r_value)
        self.label.show()
        self.grid.show()
    i = 5
