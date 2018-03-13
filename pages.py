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


from datetime import date
 
from weboob.browser.pages import JsonPage, HTMLPage
from weboob.browser.elements import ItemElement, ListElement, DictElement, method
from weboob.capabilities.weather import Forecast, Current, City, Temperature
from weboob.browser.filters.json import Dict
from weboob.browser.filters.standard import CleanText, CleanDecimal, Regexp, Format
 
 
class SearchCitiesPage(JsonPage):
    @method
    class iter_cities(DictElement):
        ignore_duplicate = True
 
        class item(ItemElement):
            klass = City
 
            def condition(self):
                return Dict('type')(self) == "VILLE_FRANCE"
 
            obj_id = Dict('codePostal')
            obj_name = Dict('slug')
 
 
class WeatherPage(HTMLPage):
    @method
    class iter_forecast(ListElement):
        item_xpath = '//div[@class="group-days-summary"]/article'
 
        class item(ItemElement):
            klass = Forecast
 
            obj_id = CleanText('./header/h4')
            obj_date = CleanText('./header/h4')
 
            def obj_low(self):
                temp = CleanDecimal(Regexp(CleanText('./ul/li[@class="day-summary-temperature"]'),
                                           '(.*) / .*'))(self)
                unit = Regexp(CleanText('./ul/li[@class="day-summary-temperature"]'), u'.*\xb0(\w) Minimale / .*')(self)
                return Temperature(float(temp), unit)
 
            def obj_high(self):
                temp = CleanDecimal(Regexp(CleanText('./ul/li[@class="day-summary-temperature"]'),
                                           '.* / (.*)'))(self)
                unit = Regexp(CleanText('./ul/li[@class="day-summary-temperature"]'), u'.* / .*\xb0(\w).*')(self)
                return Temperature(float(temp), unit)
 
            obj_text = Format('%s - %s - %s - %s',
                              CleanText('./ul/li[@class="day-summary-temperature"]'),
                              CleanText('./ul/li[@class="day-summary-image"]'),
                              CleanText('./ul/li[@class="day-summary-uv"]'),
                              CleanText('./ul/li[@class="day-summary-wind"]'))
 
    @method
    class get_current(ItemElement):
        klass = Current
 
        obj_id = date.today()
        obj_date = date.today()
        obj_text = Format('%s - %s - %s - %s',
                          CleanText('(//div[@class="group-days-summary"])[1]/article[1]/ul/li[@class="day-summary-temperature"]'),
                          CleanText('(//div[@class="group-days-summary"])[1]/article[1]/ul/li[@class="day-summary-image"]'),
                          CleanText('(//div[@class="group-days-summary"])[1]/article[1]/ul/li[@class="day-summary-uv"]'),
                          CleanText('(//div[@class="group-days-summary"])[1]/article[1]/ul/li[@class="day-summary-wind"]'))
 
        def obj_temp(self):
            temp = CleanDecimal('//div[@id="detail-day-01"]/table/tr[@class="in-between"]/td[1]')(self)
            unit = Regexp(CleanText('//div[@id="detail-day-01"]/table/tr[@class="in-between"]/td[1]'),
                          u'.*\xb0(\w)')(self)
            return Temperature(float(temp), unit)
