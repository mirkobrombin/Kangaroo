#!/usr/bin/python3
'''
   Copyright 2017 Mirko Brombin (brombinmirko@gmail.com)

   This file is part of Kangaroo.

    Kangaroo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Kangaroo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Kangaroo.  If not, see <http://www.gnu.org/licenses/>.
'''

'''
DuckDuckGo <https://duckduckgo.com>
'''
class Duck:

    path = "https://api.duckduckgo.com/?q="
    params = "&format=json&pretty=1&no_html=1&skip_disambig=1"

    @classmethod
    def search(self, query):
        # cheate url
        url = self.path+query+self.params
        # request json
        # create results list
        # return data
        return ['http://', 0, '[bang]']

def run(query):
    res = Duck.search(query)
    return res

