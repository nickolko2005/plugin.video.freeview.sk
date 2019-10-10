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

from urlparse import parse_qsl

import rtvs
import joj
import markiza

_url = sys.argv[0]
_handle = int(sys.argv[1])
_addon = xbmcaddon.Addon()
_profile = xbmc.translatePath( _addon.getAddonInfo('profile')).decode('utf-8')

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params and 'provider' in params:
        provider = params['provider']
        if provider == 'rtvs':
            prefer_mpd = xbmcplugin.getSetting(_handle, 'rtvsmpd') == 'true'
            rtvs.play(_handle, params['channel'], prefer_mpd)
        elif provider == 'joj':
            joj.play(_handle, params['channel'])
        elif provider == 'markiza':
            email = xbmcplugin.getSetting(_handle, 'mrkzemail')
            password = xbmcplugin.getSetting(_handle, 'mrkzpassword')
            markiza.play(_handle, params['channel'], email, password)
        else:
            raise #TODO
    else:
        #xbmcplugin.setPluginCategory(_handle, _addon.getLocalizedString(30000))
        #xbmcplugin.addDirectoryItem(_handle, get_url(action='new'), xbmcgui.ListItem(label=_addon.getLocalizedString(30001)), True)
        #xbmcplugin.addDirectoryItem(_handle, get_url(action='full'), xbmcgui.ListItem(label=_addon.getLocalizedString(30002)), True)
        xbmcplugin.endOfDirectory(_handle)

if __name__ == '__main__':
    router(sys.argv[2][1:])