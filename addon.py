# -*- coding: utf-8 -*-

'''
    Zouzounia TV Addon
    Author Twilight0

        License summary below, for more details please read license.txt file

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 2 of the License, or
        (at your option) any later version.
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from sys import argv
from resources.lib import navigator
from tulip.compat import parse_qsl
from tulip import control, bookmarks, cache

params = dict(parse_qsl(argv[2].replace('?', '')))

action = params.get('action')
url = params.get('url')
image = params.get('image')
title = params.get('title')
query = params.get('query')


if action is None:

    navigator.Zouzounia().main()

elif action == 'videos':

    navigator.Zouzounia().videos()

elif action == 'play':

    navigator.Zouzounia().play(url)

elif action == 'refresh':

    control.refresh()

elif action == 'playlists':

    navigator.Zouzounia().playlists()

elif action == 'youtube':

    navigator.Zouzounia().youtu(url)

elif action == 'third_party':

    navigator.Zouzounia().third_party()

elif action == 'bookmarks':

    navigator.Zouzounia().bm_list()

elif action == 'addBookmark':

    bookmarks.add(url)

elif action == 'deleteBookmark':

    bookmarks.delete(url)

elif action == 'settings':

    control.openSettings()

elif action == 'cache_clear':

    if control.yesnoDialog(line1=control.lang(30009), line2='', line3=''):

        cache.clear(withyes=False)
        control.infoDialog(control.lang(30010))

    else:

        control.infoDialog(control.lang(30011))
