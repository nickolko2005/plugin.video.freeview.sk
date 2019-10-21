# -*- coding: utf-8 -*-
# Author: cache-sk
# Created on: 10.10.2019
# License: AGPL v.3 https://www.gnu.org/licenses/agpl-3.0.html

import os
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs
import traceback

from urlparse import parse_qsl
from urllib import urlencode
from importlib import import_module

sys.path.append(os.path.join (os.path.dirname(__file__), 'resources', 'providers'))

_url = sys.argv[0]
_handle = int(sys.argv[1])
_addon = xbmcaddon.Addon()

PLAYLIST = 'special://home/addons/'+_addon.getAddonInfo('id')+'/resources/playlist.m3u'

def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs, 'utf-8'))

def info():
    xbmcgui.Dialog().textviewer(_addon.getAddonInfo('name'), _addon.getLocalizedString(30999))
    xbmcplugin.setResolvedUrl(_handle, False, xbmcgui.ListItem())

def extract():
    destination = xbmcgui.Dialog().browseSingle(3, _addon.getAddonInfo('name'), '')
    if destination is not None and destination:
        try:
            if xbmcvfs.exists(destination + 'playlist.m3u'):
                if not xbmcgui.Dialog().yesno(_addon.getAddonInfo('name'), _addon.getLocalizedString(30902)):
                    return
            xbmcvfs.copy(PLAYLIST, destination + 'playlist.m3u')
            xbmcgui.Dialog().ok(_addon.getAddonInfo('name'), _addon.getLocalizedString(30900))
        except Exception as e:
            xbmcgui.Dialog().ok(_addon.getAddonInfo('name'), _addon.getLocalizedString(30901), str(e))
    xbmcplugin.setResolvedUrl(_handle, False, xbmcgui.ListItem())

def setpisc():
    try:
        pisc = xbmcaddon.Addon('pvr.iptvsimple')
    except:
        xbmcgui.Dialog().ok(_addon.getAddonInfo('name'), _addon.getLocalizedString(30010))
        xbmcplugin.setResolvedUrl(_handle, False, xbmcgui.ListItem())
        return
    if not xbmcgui.Dialog().yesno(_addon.getAddonInfo('name'), _addon.getLocalizedString(30998)):
        xbmcplugin.setResolvedUrl(_handle, False, xbmcgui.ListItem())
        return
    pisc.setSetting('m3uPathType','0')
    pisc.setSetting('m3uPath',xbmc.translatePath(PLAYLIST))
    pisc.setSetting('startNum','1')
    pisc.setSetting('logoPathType','1')
    pisc.setSetting('logoBaseUrl','')
    pisc.setSetting('logoFromEpg','1')
    xbmcplugin.setResolvedUrl(_handle, False, xbmcgui.ListItem())

def settings():
    _addon.openSettings()
    xbmcplugin.setResolvedUrl(_handle, False, xbmcgui.ListItem())

def piscsettings():
    try:
        pisc = xbmcaddon.Addon('pvr.iptvsimple')
    except:
        xbmcgui.Dialog().ok(_addon.getAddonInfo('name'), _addon.getLocalizedString(30010))
        xbmcplugin.setResolvedUrl(_handle, False, xbmcgui.ListItem())
        return
    pisc.openSettings()
    xbmcplugin.setResolvedUrl(_handle, False, xbmcgui.ListItem())

def menu():
    xbmcplugin.addDirectoryItem(_handle, get_url(action='info'), xbmcgui.ListItem(label=_addon.getLocalizedString(30001)), False)
    xbmcplugin.addDirectoryItem(_handle, get_url(action='extract'), xbmcgui.ListItem(label=_addon.getLocalizedString(30002)), False)
    xbmcplugin.addDirectoryItem(_handle, get_url(action='setpisc'), xbmcgui.ListItem(label=_addon.getLocalizedString(30003)), False)
    xbmcplugin.addDirectoryItem(_handle, get_url(action='settings'), xbmcgui.ListItem(label=_addon.getLocalizedString(30004)), False)
    xbmcplugin.addDirectoryItem(_handle, get_url(action='piscsettings'), xbmcgui.ListItem(label=_addon.getLocalizedString(30005)), False)
    xbmcplugin.endOfDirectory(_handle)

def router(paramstring):
    try:
        params = dict(parse_qsl(paramstring))
        if params:
            if 'provider' in params:
                provider = params['provider']
                module = import_module(provider)
                module.play(_handle, _addon, params)
            elif 'action' in params:
                globals()[params['action']]()
            else:
                menu()
        else:
            menu()
    except Exception as e:
        xbmcgui.Dialog().ok(_addon.getAddonInfo('name'), str(e))
        traceback.print_exc()

if __name__ == '__main__':
    router(sys.argv[2][1:])