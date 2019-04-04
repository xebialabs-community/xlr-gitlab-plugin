#
# Copyright 2019 XEBIALABS
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
        if event["event_type"].lower() == "merge_request":
            logger.info("Found pull request event for template %s " % template_filter)
            handle_push_event(event, template_filter)
    except:
        e = sys.exc_info()[1]
        msg = ("Could not parse payload, check your Gitlab Webhook "
               "configuration. Error: %s. Payload:\n%s" % (e, event))
        logger.warn(msg)
        return

def handle_push_event(event, template_filter):
    proj_name = str(event["project"]["name"])
    repo_name = str(event["repository"]["name"])
    pr_number = str(event['object_attributes']['iid'])
    pr_title = str(event['object_attributes']['title'])
    source_hash = str(event['object_attributes']['last_commit']['id'])
    source_branch = str(event['object_attributes']['source_branch'])
    source_project = str(event['object_attributes']['source']['name'])
    source_repo = str(event['object_attributes']['source']['name'])
    target_branch = str(event['object_attributes']['target_branch'])
    target_project = str(event['object_attributes']['target']['name'])
    target_repo = str(event['object_attributes']['target']['name'])
    logger.info("Starting release for Pull Request %s" %  pr_number)
    start_pr_release(proj_name, repo_name, pr_number, pr_title, source_hash, source_branch,source_project, source_repo, target_branch,target_project, target_repo, template_filter)




def start_pr_release(proj_name, repo_name, pr_number, pr_title, source_hash,source_branch,source_project, source_repo, target_branch,target_project, target_repo, template_filter = None):
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
    params.setReleaseTitle('Pull Request #%s: %s' % (pr_number, pr_title))
    variables = HashMap()
    variables.put('${pull_request_number}', '%s' % pr_number)
    variables.put('${pull_request_title}', '%s' % pr_title)
    variables.put('${repository_name}', '%s' % repo_name)
    variables.put('${proj_name}', '%s' % proj_name)
    variables.put('${source_hash}', '%s' % source_hash)
    variables.put('${source_branch}', '%s' % source_branch)
    variables.put('${source_project}', '%s' % source_project)
    variables.put('${source_repo}', '%s' % source_repo)
    variables.put('${target_branch}', '%s' % target_branch)
    variables.put('${target_project}', '%s' % target_project)
    variables.put('${target_repo}', '%s' % target_repo)
    params.setReleaseVariables(variables)
    started_release = templateApi.start(template_id, params)
    response.entity = started_release
    logger.info("Started release %s for Pull Request %s" % (started_release.getId(), pr_number))

handle_request(request.entity, request.query['template'])