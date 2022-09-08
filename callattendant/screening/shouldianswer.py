#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
#  nomorobo.py
#
#  Copyright 2018 Bruce Schubert <bruce@emxsys.com>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.


import urllib.request
from bs4 import BeautifulSoup


class ShouldIAnswerService(object):

    def lookup_number(self, number):
        url = "https://www.shouldianswer.com/search?q=%s" % number
        #print(url)
        headers = {}
        allowed_codes = [404]  # allow not found response
        content = self.http_get(url, headers, allowed_codes)
        soup = BeautifulSoup(content, "lxml")  # lxml HTML parser: fast

        spam = False
        reason = ""

        try:
            scoreContainer = soup.findAll("div", class_="scoreContainer")[0]
            scoreDiv = scoreContainer.findChildren("div")[0]
            if "negative" in scoreDiv["class"]:
                spam = True
            elif "unknown" in scoreDiv["class"]:
                reason = "Unknown"
        except Exception as e:
            print("Could not get score:", e)

        try:
            categories = soup.findAll("div", class_="categories")[0]
            reason = categories.findChildren("li")[0].get_text()
            reason = reason.replace("\n", "").strip(" ")
        except Exception as e:
            print("Could not get reason:", e)

        result = {
            "spam": spam,
            "reason": reason
        }
        return result

    def http_get(self, url, add_headers={}, allowed_codes=[]):
        data = ""
        try:
            request = urllib.request.Request(url, headers=add_headers)
            response = urllib.request.urlopen(request, timeout=5)
            data = response.read()
        except urllib.error.HTTPError as e:
            code = e.getcode()
            if code not in allowed_codes:
                raise
            data = e.read()
        return data
