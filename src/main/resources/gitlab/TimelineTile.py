#
#
# Copyright 2021 XEBIALABS
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

client = Client()
commits = json.loads(client.gitlab_querycommits(locals())["commits"])

# Compile data for summary view
commitsByDay = {}
for commit in commits:
    commitDate = convertRFC3339ToDate(commit["committed_date"])
    if commitDate in commitsByDay.keys():
        commitsByDay[commitDate] += 1
    else:
        commitsByDay[commitDate] = 1

dates = [date for date in commitsByDay.keys()]
dates.sort()
startDate = dates[0]
endDate = dates[-1]
days = []
commitsEachDay = []
daysWithCommits = [dayCommits.toString() for dayCommits in commitsByDay.keys()]
while startDate.isBefore(endDate.plusDays(1)):
    days.append(startDate.toString())
    if startDate.toString() in daysWithCommits:
        commitsEachDay.append(commitsByDay[startDate])
    else:
        commitsEachDay.append(0)
    startDate = startDate.plusDays(1)

data = {"dates": days, "commitsEachDay": commitsEachDay, "commits": commits}
