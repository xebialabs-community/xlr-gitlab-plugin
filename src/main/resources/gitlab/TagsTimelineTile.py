#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
from gitlab.Client import Client
from java.time import LocalDate, ZonedDateTime

def convertRFC3339ToDate(timestamp):
    zonedDateTime = ZonedDateTime.parse(timestamp)
    return zonedDateTime.toLocalDate()

tags = json.loads(Client.gitlab_querytags(locals())["tags"])

# Compile data for summary view
tagsByDay = {}
tagNamesByDay = {}
for tag in tags:
    tagDate = convertRFC3339ToDate(tag["commit"]["committed_date"])
    if tagDate in tagsByDay.keys():
        tagsByDay[tagDate] += 1
        tagNamesByDay[tagDate] = tagNamesByDay[tagDate] + ", " + tag["name"]
    else:
        tagsByDay[tagDate] = 1
        tagNamesByDay[tagDate] = tag["name"]

if len(tagsByDay) == 0:
    raise Exception("No tags found for ")

dates = [date for date in tagsByDay.keys()]
dates.sort()
startDate = dates[0]
endDate = dates[-1]
days = []
tagsEachDay = []
tagNamesEachDay = []
daysWithTags = [dayTags.toString() for dayTags in tagsByDay.keys()]
while startDate.isBefore(endDate.plusDays(1)):
    days.append(startDate.toString())
    if startDate.toString() in daysWithTags:
        tagsEachDay.append(tagsByDay[startDate])
        tagNamesEachDay.append(tagNamesByDay[startDate])
    else:
        tagsEachDay.append(0)
        tagNamesEachDay.append("None")
    startDate = startDate.plusDays(1)

data = {
    "dates": days,
    "tagsEachDay": tagsEachDay,
    "tagNamesEachDay": tagNamesEachDay,
    "tags": tags
}