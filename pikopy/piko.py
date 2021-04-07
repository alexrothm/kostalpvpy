#!/usr/bin/env python

# The MIT License (MIT)
#
# Copyright (c) 2014 Christian Stade-Schuldt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Library to work with a Piko inverter from Kostal."""

import urllib.request
from lxml import html


class Piko():
    def __init__(self, host=None, username='pvserver', password='pvwr'):
        self.host = host
        self.username = username
        self.password = password

    def get_logdaten_dat(self):
        pass

    def get_current_power(self):
        """returns the current power in W"""
        tmp = self._get_raw_content()[0]
        if not tmp.isnumeric():
            return 0
        return int(tmp)

    def get_total_energy(self):
        """returns the total energy in kWh"""
        tmp = self._get_raw_content()[1]
        if not tmp.isnumeric():
            return 0
        return int(self._get_raw_content()[1])

    def get_daily_energy(self):
        """returns the daily energy in kWh"""
        tmp = self._get_raw_content()[2]
        if not tmp.isnumeric():
            return 0
        return float(self._get_raw_content()[2])

    def get_string1_voltage(self):
        tmp = self._get_raw_content()[3]
        if not tmp.isnumeric():
            return 0
        """returns the voltage from string 1 in V"""
        return int(self._get_raw_content()[3])

    def get_string1_current(self):
        """returns the current from string 1 in A"""
        tmp = self._get_raw_content()[5]
        if not tmp.isnumeric():
            return 0
        return float(self._get_raw_content()[5])

    def get_string2_voltage(self):
        """returns the voltage from string 2 in V"""
        tmp = self._get_raw_content()[7]
        if not tmp.isnumeric():
            return 0
        return int(self._get_raw_content()[7])

    def get_string2_current(self):
        """returns the current from string 2 in A"""
        tmp = self._get_raw_content()[9]
        if not tmp.isnumeric():
            return 0
        return float(self._get_raw_content()[9])

    def get_string3_voltage(self):
        """returns the voltage from string 3 in V"""
        tmp = self._get_raw_content()[11]
        if not tmp.isnumeric():
            return 0
        return int(self._get_raw_content()[11])

    def get_string3_current(self):
        """returns the current from string 3 in A"""
        tmp = self._get_raw_content()[13]
        if not tmp.isnumeric():
            return 0
        return float(self._get_raw_content()[13])

    def get_l1_voltage(self):
        """returns the voltage from line 1 in V"""
        tmp = self._get_raw_content()[4]
        if not tmp.isnumeric():
            return 0
        return int(self._get_raw_content()[4])

    def get_l1_power(self):
        """returns the power from line 1 in W"""
        tmp = self._get_raw_content()[6]
        if not tmp.isnumeric():
            return 0
        return int(self._get_raw_content()[6])

    def get_l2_voltage(self):
        """returns the voltage from line 2 in V"""
        tmp = self._get_raw_content()[8]
        if not tmp.isnumeric():
            return 0
        return int(self._get_raw_content()[8])

    def get_l2_power(self):
        """returns the power from line 1 in W"""
        tmp = self._get_raw_content()[10]
        if not tmp.isnumeric():
            return 0
        return int(self._get_raw_content()[10])

    def get_l3_voltage(self):
        """returns the voltage from line 3 in V"""
        tmp = self._get_raw_content()[12]
        if not tmp.isnumeric():
            return 0
        return int(self._get_raw_content()[12])

    def get_l3_power(self):
        """returns the power from line 3 in W"""
        tmp = self._get_raw_content()[14]
        if not tmp.isnumeric():
            return 0
        return int(self._get_raw_content()[14])

    def get_status(self):
        """returns the status of the inverter"""
        return self._get_raw_content()[15]

    def _get_raw_content(self):
        """returns all values as a list"""
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.host, self.username, self.password)
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        opener.open(self.host)

        urllib.request.install_opener(opener)
        response = urllib.request.urlopen(self.host)
        root = html.fromstring(response.read().strip())
        data = [v.text.strip() for v in root.xpath("//td[@bgcolor='#FFFFFF']")]
        data.append(root.xpath("//td[@colspan='4']")[0].text.strip())
        return data
