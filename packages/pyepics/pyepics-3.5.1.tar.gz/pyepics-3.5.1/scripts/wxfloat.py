#!/usr/bin/python
#
# simple PV Probe application

import wx
import sys
import epics
from epics.wx import EpicsFunction, DelayedEpicsCallback, PVFloatCtrl

class PVDisplay(wx.Frame):
    def __init__(self, pvname=None, **kws):
        wx.Frame.__init__(self, None, wx.ID_ANY,  **kws)
        self.SetFont(wx.Font(11,wx.SWISS,wx.NORMAL,wx.BOLD,False))
        self.pvname = pvname

        self.SetTitle("%s" % pvname)

        self.sizer = wx.GridBagSizer(3, 2)
        panel = wx.Panel(self)
        self.ctrl = PVFloatCtrl(panel, self.pvname, act_on_losefocus=True, size=(200, -1))
        self.name = wx.StaticText(panel, label=pvname,        size=(120, -1))

        self.sizer.Add(self.name,  (0, 0), (1, 1), wx.EXPAND, 1)
        self.sizer.Add(self.ctrl,  (0, 1), (1, 1), wx.EXPAND, 1)

        panel.SetSizer(self.sizer)

        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(panel, 1, wx.EXPAND, 2)
        s.Fit(self)
        self.Refresh()
        # self.connect_pv()

if __name__ == '__main__':
    app = wx.App(redirect=False)
    pv = epics.caget('13IDE:m34.VAL')
    epics.poll()
    PVDisplay(pvname='13IDE:m34.VAL').Show()
    app.MainLoop()
