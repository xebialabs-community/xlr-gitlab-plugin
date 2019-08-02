#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from gitlab.Client import Client

import json


def findNewCommit(oldCommitMap, newCommitMap):
    branch = ""
    commitId = ""

    # loop over new map branches
    for newBranch, newCommitId in newCommitMap.iteritems():
        # check if branch exists in old map
        if newBranch in oldCommitMap:
            oldCommitId = oldCommitMap[newBranch]
            # compare commit ids
            if newCommitId != oldCommitId:
                branch = newBranch
                commitId = newCommitId
                break
        else:
            # new branch, this triggered it
            branch = newBranch
            commitId = newCommitId
            break

    return branch, commitId


if gitlab_server is None:
    raise Exception("No GitLab server provided.")

client = Client.get_client()
latestCommits = client.gitlab_branch_statuses(locals())

# trigger state is persisted as json
newTriggerState = json.dumps(latestCommits)

if triggerState != latestCommits:
    if len(triggerState) == 0:
        oldCommits = {}
    else:
        oldCommits = json.loads(triggerState)

    branch, commitId = findNewCommit(oldCommits, latestCommits)

    if not branchName or (branchName and branchName == branch):
        triggerState = newTriggerState

print("GitLab triggered release for %s %s" % (branch, commitId))
