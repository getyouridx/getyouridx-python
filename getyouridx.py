'''
Copyright 2009  GetYourIDX (email : info@getyouridx.com)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


Created on Nov 11, 2009
@author: Paul Trippett (paul@getyourview.com)
@copyright: 2009 GetYourView LLC
@organization: GetYourView LLC
'''


import urllib
from xml.dom import minidom


class IDXException(Exception):
    """
    The IDXException class represents exceptions raised.
    @category   IDX
    @package    IDX
    @copyright  Copyright (c) GetYourIDX.com. (http://www.getyouridx.com)
    @license    GNU General Public License
    """
    pass    

class IDXFilter:
    """
    The IDXFilter interface represents classes used to specify IDX data result filters.
    @category   IDX
    @package    IDX
    @copyright  Copyright (c) GetYourIDX.com. (http://www.getyouridx.com)
    @license    GNU General Public License
    """
    def toString(self):
        pass

class IDXFilter_Limit(IDXFilter):
    """
    The IDXFilter_Limit class specifies a filter to limit the result.
    @category   IDX
    @package    IDX
    @copyright  Copyright (c) GetYourIDX.com. (http://www.getyouridx.com)
    @license    GNU General Public License
    """
    limit = 0
    def __init__(self, limit):
        self.limit = limit
    
    def toString(self):
        return "&limit=" + str(self.limit)

class IDXFilter_Format(IDXFilter):
    """
    The IDXFilter_Format class specifies a filter to format the result.
    @category   IDX
    @package    IDX
    @copyright  Copyright (c) GetYourIDX.com. (http://www.getyouridx.com)
    @license    GNU General Public License
    """
    format = 'xml'
    def __init__(self, format):
        self.format = format
    
    def toString(self):
        return "&format=" + str(self.format)

class IDXFilter_Range(IDXFilter):
    """
    The IDXFilter_Range class specifies a filter based a range.
    @category   IDX
    @package    IDX
    @copyright  Copyright (c) GetYourIDX.com. (http://www.getyouridx.com)
    @license    GNU General Public License
    """
    field = ''
    min = 0
    max = 0
    def __init__(self, field, min, max):
        self.field = field
        self.min = min
        self.max = max
    
    def toString(self):
        return "&fge_" + str(self.field) + "=" + str(self.min) + "&fle_" + str(self.field) + "=" + str(self.max)

class IDXFilter_Offset(IDXFilter):
    """
    The IDXFilter_Offset class specifies a filter to specify the paging offset.
    @category   IDX
    @package    IDX
    @copyright  Copyright (c) GetYourIDX.com. (http://www.getyouridx.com)
    @license    GNU General Public License
    """
    offset = 0
    def __init__(self, offset):
        self.offset = offset
    
    def toString(self):
        return "&offset=" + str(self.offset)

class IDXFilter_Sort(IDXFilter):
    """
    The IDXFilter_Sort class specifies a filter on sort the query.
    @category   IDX
    @package    IDX
    @copyright  Copyright (c) GetYourIDX.com. (http://www.getyouridx.com)
    @license    GNU General Public License
    """
    field = ''
    direction = 'ASC'
    def __init__(self, field, direction):
        self.field = field
        self.direction = direction
    
    def toString(self):
        return "&sort=" + str(self.field) + ":" + str(self.direction)

class IDXFilter_LessThan(IDXFilter):
    """
    The IDXFilter_LessThan class specifies a filter to query a field with a LessThan operator.
    @category   IDX
    @package    IDX
    @copyright  Copyright (c) GetYourIDX.com. (http://www.getyouridx.com)
    @license    GNU General Public License
    """
    field = ''
    value = 0
    def __init__(self, field, value):
        self.field = field
        self.value = value
    
    def toString(self):
        return "&fle_" + str(self.field) + "=" + str(self.value)

class IDXFilter_GreaterThan(IDXFilter):
    """
    The IDXFilter_GreaterThan class specifies a filter to query a field with a GreaterThan operator.
    @category   IDX
    @package    IDX
    @copyright  Copyright (c) GetYourIDX.com. (http://www.getyouridx.com)
    @license    GNU General Public License
    """
    field = ''
    value = 0
    def __init__(self, field, value):
        self.field = field
        self.value = value
    
    def toString(self):
        return "&fge_" + str(self.field) + "=" + str(self.value)

class IDXFilter_Equals(IDXFilter):
    """
    The IDXFilter_Equals class specifies a filter to query a field with an Equals operator.
    @category   IDX
    @package    IDX
    @copyright  Copyright (c) GetYourIDX.com. (http://www.getyouridx.com)
    @license    GNU General Public License
    """
    field = ''
    value = 0
    def __init__(self, field, value):
        self.field = field
        self.value = value
    
    def toString(self):
        return "&feq_" + str(self.field) + "=" + str(self.value)

class IDXFilter_In(IDXFilter):
    """
    The IDXFilter_In class specifies a filter to query a field where the value is equal to one of the passed array items.
    @category   IDX
    @package    IDX
    @copyright  Copyright (c) GetYourIDX.com. (http://www.getyouridx.com)
    @license    GNU General Public License
    """
    field = ''
    value = []
    def __init__(self, field, value):
        self.field = field
        self.value = value
    
    def toString(self):
        return "&fin_" + str(self.field) + "=" + ",".join(self.value)

class IDXSearch:
    """
    The IDXSearch class allows requesting data from the GetYourIDX Service based on a number of filters.
    @category   IDX
    @package    IDX
    @copyright  Copyright (c) GetYourIDX.com. (http://www.getyouridx.com)
    @license    GNU General Public License
    """
    apikey = ''
    service_url = 'http://www.getyouridx.com/api/property/'
    filters = []
    def __init__(self, apikey):
        self.apikey = apikey
    def add_filter(self, filter):
        self.filters.append(filter)
    def result(self):
        return minidom.parse(urllib.urlopen(self.service_url + self.build_querystring()))
    def build_querystring(self):
        querystring = '?apikey=' + self.apikey;
        for filter in self.filters:
            querystring = querystring + filter.toString()
        return querystring

class IDXCity:
    """
    The IDXCity class allows requesting cities from the MLSID
    @category   IDX
    @package    IDX
    @copyright  Copyright (c) GetYourIDX.com. (http://www.getyouridx.com)
    @license    GNU General Public License
    """
    apikey = ''
    service_url = 'http://www.getyouridx.com/api/city/'
    def __init__(self, apikey):
        self.apikey = apikey
    def getByMLS(self, mls):
        return minidom.parse(urllib.urlopen(self.service_url + "?apikey=" + self.apikey + "&fin_mls_id=" + mls))
