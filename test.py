# -*- coding: utf-8 -*-

# Copyright(C) 2018      liyapo
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals


from weboob.tools.test import BackendTest


class AccuweatherTest(BackendTest):
    MODULE = 'accuweather'
 
    def test_accuweather(self):
        l = list(self.backend.iter_city_search('Anadyr'))
        self.assertTrue(len(l) > 0)
 
        city = l[0]
        current = self.backend.get_current(city.id)
	self.assertTrue(current.temp.value is float(current.temp.value))
 
        forecasts = list(self.backend.iter_forecast(city.id))
        self.assertTrue(len(forecasts) > 1)
 
#        forecast2 = list(self.backend.iter_forecast('blagnac'))
#        self.assertTrue(len(forecast2) > 0)
