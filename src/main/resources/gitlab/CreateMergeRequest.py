#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string
import com.xhaus.jyson.JysonCodec as json

if gitLabServer is None:
    print "No server provided"
    sys.exit(1)

gitlabURL = gitLabServer['url']
if gitlabURL.endswith('/'):
    gitlabURL = gitlabURL[:len(gitlabURL)-1]

if APIKey == None:
    if gitLabServer['APIKey'] <> None:
        APIKey = gitLabServer['APIKey']
    else:
        print "API Key not set"
        sys.exit(1)

content="source_branch=" + source_branch + "&target_branch=" + target_branch + "&title=" + title
request = HttpRequest(gitLabServer)
response = request.post('/api/v3/projects/' + project_id + '/merge_requests?private_token=' + APIKey, content, contentType = '')

if response.status < 400:
    data = json.loads(response.response)
    mergeId = data.get('id')
    print "Created %s in JIRA at %s." % (mergeId, gitlabURL)
else:
    print "Failed to create merge request at %s." % gitlabURL
    response.errorDump()
    sys.exit(1)
