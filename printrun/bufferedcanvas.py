"""
BufferedCanvas -- flicker-free canvas widget
Copyright (C) 2005, 2006 Daniel Keep, 2011 Duane Johnson

To use this widget, just override or replace the draw method.
This will be called whenever the widget size changes, or when
the update method is explicitly called.

Please submit any improvements/bugfixes/ideas to the following
url:

  http://wiki.wxpython.org/index.cgi/BufferedCanvas

2006-04-29: Added bugfix for a crash on Mac provided by Marc Jans.
"""

# Hint: try removing '.sp4msux0rz'
__author__ = 'Daniel Keep <daniel.keep.sp4msux0rz@gmail.com>'

__license__ = """
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation; either version 2.1 of the
License, or (at your option) any later version.

As a special exception, the copyright holders of this library
hereby recind Section 3 of the GNU Lesser General Public License. This
means that you MAY NOT apply the terms of the ordinary GNU General
Public License instead of this License to any given copy of the
Library. This has been done to prevent users of the Library from being
denied access or the ability to use future improvements.

This library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""

__all__ = ['BufferedCanvas']

import wx

class BufferedCanvas(wx.Panel):
    """
    Implements a flicker-free canvas widget.

    Standard usage is to subclass this class, and override the
    draw method.  The draw method is passed a device context, which
    should be used to do your drawing.

    If you want to force a redraw (for whatever reason), you should
    call the update method.  This is because the draw method is never
    called as a result of an EVT_PAINT event.
    """

    # These are our two buffers.  Just be aware that when the buffers
    # are flipped, the REFERENCES are swapped.  So I wouldn't want to
    # try holding onto explicit references to one or the other ;)
    buffer = None
    backbuffer = None

    def __init__(self,
                 parent,
                 ID=-1,
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 style = wx.NO_FULL_REPAINT_ON_RESIZE|wx.WANTS_CHARS):
        wx.Panel.__init__(self, parent, ID, pos, size, style)

        # Bind events
        self.Bind(wx.EVT_PAINT, self.onPaint)

        # Disable background erasing (flicker-licious)
        def disable_event(*pargs,**kwargs):
            pass # the sauce, please
        self.Bind(wx.EVT_ERASE_BACKGROUND, disable_event)

    ##
    ## General methods
    ##

    def draw(self, dc):
        """
        Stub: called when the canvas needs to be re-drawn.
        """
        pass

    def update(self):
        """
        Causes the canvas to be updated.
        """
        self.Refresh()

    def getWidthHeight(self):
        width, height = self.GetClientSizeTuple()
        if width == 0:
            width = 1
        if height == 0:
            height = 1
        return (width, height)

    ##
    ## Event handlers
    ##

    def onPaint(self, event):
        # Blit the front buffer to the screen
        w, h = self.GetClientSizeTuple()
        if not w or not h:
            return
        else:
            dc = wx.BufferedPaintDC(self)
            self.draw(dc, w, h)
