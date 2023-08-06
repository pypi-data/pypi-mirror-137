# -*- coding: utf-8 -*-

# hikingmap -- render maps on paper using data from OpenStreetMap
# Copyright (C) 2015  Roel Derickx <roel.derickx AT gmail>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import math
from lxml import etree

class Coordinate:
    # lon and lat are coordinates, by default in degrees
    def __init__(self, lon, lat, isDegrees = True):
        if isDegrees:
            self.set_lon(lon)
            self.set_lat(lat)
        else:
            self.lon = math.degrees(lon)
            self.lat = math.degrees(lat)
            self.lon_radians = lon
            self.lat_radians = lat


    def __copy__(self):
        return Coordinate(self.lon, self.lat, True)


    def set_lon(self, lon):
        self.lon = lon
        self.lon_radians = math.radians(lon)


    def set_lat(self, lat):
        self.lat = lat
        self.lat_radians = math.radians(lat)


    def equals(self, coord):
        return self.lon == coord.lon and self.lat == coord.lat


    # calculate bearing between self and coord
    def bearing(self, coord):
        d_lon = coord.lon_radians - self.lon_radians

        y = math.sin(d_lon) * math.cos(coord.lat_radians)
        x = math.cos(self.lat_radians) * math.sin(coord.lat_radians) - \
            math.sin(self.lat_radians) * math.cos(coord.lat_radians) * math.cos(d_lon)
        return math.atan2(y, x)


    @staticmethod
    def __get_earth_radius(length_unit):
        if length_unit == "mi":
            return 3959
        else: # default to km
            return 6371


    def distance_haversine(self, coord, length_unit):
        '''
        Calculates distance in km or mi between self and coord
        '''
        d_lat = coord.lat_radians - self.lat_radians
        d_lon = coord.lon_radians - self.lon_radians

        a = math.sin(d_lat/2) * math.sin(d_lat/2) + \
            math.sin(d_lon/2) * math.sin(d_lon/2) * \
            math.cos(self.lat_radians) * math.cos(coord.lat_radians)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return self.__get_earth_radius(length_unit) * c


    def calc_waypoint_on_line(self, dest_coord, distance, length_unit):
        '''
        Returns the coordinate of the point which is on a given distance
        from self in the direction of dest_coord
        '''
        b = self.bearing(dest_coord)
        earth_radius = self.__get_earth_radius(length_unit)
        return Coordinate(#lon
                          self.lon_radians + \
                          math.atan2(math.sin(b) * \
                                     math.sin(distance/earth_radius) * \
                                     math.cos(self.lat_radians), \
                                     math.cos(distance/earth_radius) - \
                                     math.sin(self.lat_radians) * \
                                     math.sin(dest_coord.lat_radians)), \
                          #lat
                          math.asin(math.sin(self.lat_radians) * \
                                    math.cos(distance/earth_radius) + \
                                    math.cos(self.lat_radians) * \
                                    math.sin(distance/earth_radius) * \
                                    math.cos(b)),
                          False)


    def to_string(self):
        return str(round(self.lon, 6)) + "," + str(round(self.lat, 6))


    def to_xml(self, tagname, description):
        wayptattrs = { 'lat':('%.15f' % self.lat), \
                       'lon':('%.15f' % self.lon) }
        wayptnode = etree.Element(tagname, wayptattrs)

        if description:
            wayptnamenode = etree.Element('name')
            wayptnamenode.text = description
            wayptnode.append(wayptnamenode)

        return wayptnode
