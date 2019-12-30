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
import sys

client = Client.get_client()
response = client.gitlab_pipeline_status(locals())
if response is not None:
    for key, value in response.items():
        locals()[key] = value

task.setStatusLine(
    "Pipeline #{0}:{1} ".format(response["pipeline_id"], response["status"])
)
pipeline_status = response["status"]
pipeline_web_url = response["web_url"]

if response["status"] == "pending":
    task.schedule("gitlab/pipeline-wait.py")

if response["status"] == "running":
    task.schedule("gitlab/pipeline-wait.py")

if response["status"] == "failed":
    print "Pipeline #{0}: {1}".format(response["pipeline_id"], "Failed!")
    pipeline_status = "failed"
    sys.exit(1)

if response["status"] == "success":
    print "Pipeline #{0}: {1}".format(response["pipeline_id"], "Success!")
    pipeline_status = "success"
