#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


from com.xebialabs.xlrelease.api.v1.forms import StartRelease
from java.util import HashMap
import sys


def handle_request(event, template_filter = None):
    
    try:
       if event["event_name"].lower() == "push":
           logger.info("Found push event for template %s " % template_filter)
           handle_push_event(event, template_filter)
    except:
       e = sys.exc_info()[1]
       msg = ("Could not parse payload, check your Gitlab Webhook "
              "configuration. Error: %s. Payload:\n%s" % (e, event))
       logger.warn(msg)
       return

def handle_push_event(event, template_filter):

	current_commit_hash = str(event["checkout_sha"])
	commit_message = str(event["message"])
	ref = str(event["ref"])
	project_name = str(event["project"]["name"])
	repository_name = str(event["repository"]["name"])
	logger.info("Starting release for new branch %s in repository %s from template %s" % ( repository_name, ref, template_filter))
	start_new_branch_release(repository_name, project_name, ref, current_commit_hash, commit_message, template_filter)



def start_new_branch_release(repo_full_name, project_name, branch_name, current_commit_hash, commit_message, template_filter = None):
	templates = templateApi.getTemplates(template_filter)
	if not templates:
		response.statusCode = 500
		raise Exception("Could not find any templates by filter : %s " % template_filter)
	else:
		if len(templates) > 1:
			response.statusCode = 500
			raise Exception("Found more than one template with tag '%s', please use more specific value. List Found : %s" % (template_filter, [item.title for item in templates]))
	
	template_id = templates[0].id
	params = StartRelease()
	params.setReleaseTitle("Release for [%s]:[%s]:[%s]" % (project_name, repo_full_name, branch_name))
	variables = HashMap()
	variables.put('${project_name}', '%s' % project_name)
	variables.put('${repo_full_name}', '%s' % repo_full_name)
	variables.put('${branch_name}', '%s' % branch_name)
	variables.put('${commit_message}', '%s' % commit_message)
	variables.put('${current_commit_hash}', '%s' % current_commit_hash)
	params.setReleaseVariables(variables)
	started_release = templateApi.start(template_id, params)
	response.entity = started_release
	logger.info("Started Release %s for [%s]:[%s]:[%s]" % (started_release.getId(),project_name, repo_full_name, branch_name))

handle_request(request.entity, request.query['template'])