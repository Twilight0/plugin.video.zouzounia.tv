# -*- coding: utf-8 -*-

"""
    Zouzounia TV Addon
    Author: Twilight0

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import json
from base64 import b64decode
from tulip import youtube, directory, control, cache, bookmarks, client
from tulip.compat import iteritems
from youtube_resolver import resolve as resolver

if control.setting('language') == '0':
    if control.infoLabel('System.Language') == 'Greek':
        main_id = 'UC9QSJuIBLUT2GbjgKymkTaQ'
    elif control.infoLabel('System.Language') == 'Japanese':
        main_id = 'UCGVTSfgmHJBzpq1gVq1ofhA'
    else:
        main_id = 'UCzsQf6eiWz4gIHgx0oYadXA'
elif control.setting('language') == '2':
    main_id = 'UC9QSJuIBLUT2GbjgKymkTaQ'
elif control.setting('language') == '3':
    main_id = 'UCGVTSfgmHJBzpq1gVq1ofhA'
else:
    main_id = 'UCzsQf6eiWz4gIHgx0oYadXA'


key = b64decode('zNHTHh1STN3SzVERB9kUmFWVmlkUFJ1UwYHZZJkUh5kQ5NVY6lUQ'[::-1])  # please do not copy this key


class Zouzounia:
    
    def __init__(self):

        self.list = []

    def main(self):

        self.list = [
            {
                'title': control.lang(30001),
                'action': 'videos',
                'icon': 'videos.jpg'
            }
            ,
            {
                'title': control.lang(30002),
                'action': 'playlists',
                'icon': 'playlists.jpg'
            }
            ,
            {
                'title': control.lang(30003),
                'action': 'bookmarks',
                'icon': 'heart.jpg'
            }
            ,
            {
                'title': control.lang(30004),
                'action': 'settings',
                'icon': 'settings.jpg',
                'isFolder': 'False',
                'isPlayable': 'False'
            }

        ]

        cc = {'title': 30005, 'query': {'action': 'cache_clear'}}

        for item in self.list:
            item.update({'cm': [cc]})

        directory.add(self.list)
    
    def item_list(self):
    
        return youtube.youtube(key=key).videos(main_id, limit=10)

    def _playlists(self):

        return youtube.youtube(key=key).playlists(main_id, limit=10)

    def playlists(self):
    
        self.list = cache.get(self._playlists, 24)
    
        for p in self.list:
            p.update({'action': 'youtube'})

        for p in self.list:
            bookmark = dict((k, v) for k, v in iteritems(p) if not k == 'next')
            bookmark['bookmark'] = p['url']
            bm_cm = {'title': 30006, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
            refresh = {'title': 30008, 'query': {'action': 'refresh'}}
            cache_clear = {'title': 30005, 'query': {'action': 'cache_clear'}}
            p.update({'cm': [refresh, cache_clear, bm_cm]})

        directory.add(self.list)
    
    def youtu(self, plink):
    
        self.list = cache.get(youtube.youtube(key=key).playlist, 12, plink)

        if self.list is None:
            return

        for v in self.list:
            try:
                title = v['title'].decode('utf-8')
            except AttributeError:
                title = v['title']
            v.update({'action': 'play', 'isFolder': 'False', 'title': client.replaceHTMLCodes(title)})

        for item in self.list:
            bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
            bookmark['bookmark'] = item['url']
            bm_cm = {'title': 30006, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
            refresh = {'title': 30008, 'query': {'action': 'refresh'}}
            cache_clear = {'title': 30005, 'query': {'action': 'cache_clear'}}
            item.update({'cm': [refresh, cache_clear, bm_cm]})

        directory.add(self.list)
    
    def videos(self):
    
        self.list = cache.get(self.item_list, 12)

        for v in self.list:
            try:
                title = v['title'].decode('utf-8')
            except AttributeError:
                title = v['title']
            v.update({'action': 'play', 'isFolder': 'False', 'title': client.replaceHTMLCodes(title)})

        for item in self.list:
            bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
            bookmark['bookmark'] = item['url']
            bm_cm = {'title': 30006, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
            refresh = {'title': 30008, 'query': {'action': 'refresh'}}
            cache_clear = {'title': 30005, 'query': {'action': 'cache_clear'}}
            item.update({'cm': [refresh, cache_clear, bm_cm]})
    
        directory.add(self.list)
    
    def bm_list(self):
    
        bm = bookmarks.get()

        na = [{'title': 30012, 'action': None, 'icon': 'not-found.jpg'}]
    
        if not bm:
            directory.add(na)
            return na

        for item in bm:
            bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
            bookmark['delbookmark'] = item['url']
            item.update({'cm': [{'title': 30007, 'query': {'action': 'deleteBookmark', 'url': json.dumps(bookmark)}}]})
    
        self.list = sorted(bm, key=lambda k: k['title'].lower())

        directory.add(self.list)

    @staticmethod
    def session(link):

        streams = resolver(link)

        try:
            addon_enabled = control.addon_details('inputstream.adaptive').get('enabled')
        except KeyError:
            addon_enabled = False

        if not addon_enabled:
            streams = [s for s in streams if 'mpd' not in s['title'].lower()]

        stream = streams[0]['url']

        return stream

    def play(self, url):

        stream = self.session(url)

        directory.resolve(stream, dash='.mpd' in stream)
