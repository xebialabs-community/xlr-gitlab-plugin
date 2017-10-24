#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json, sys
from xlrelease.HttpRequest import HttpRequest

class Client(object):
    def __init__(self):
        return

    @staticmethod
    def get_client():
        return Client()

    @staticmethod
    def get_gitlab_server(variables):
        gitlab_server = variables['gitlab_server']
        if gitlab_server is None:
            raise Exception("No GitLab Server provided!")
        return gitlab_server

    @staticmethod
    def get_gitlab_url(gitlab_server):
        gitlab_url = gitlab_server['url']
        if gitlab_url.endswith('/'):
            gitlab_url  = gitlab_url[:len(gitlab_url) - 1]
        return gitlab_url

    @staticmethod
    def get_gitlab_api_key(gitlab_server, variables):
        if variables['api_key'] is None:
            if variables['gitlab_server']['api_key'] is not None:
                return gitlab_server['api_key']
            else:
                raise Exception("API Key Not Set!")
        else:
            return variables['api_key']

    @staticmethod
    def handle_response(response):
        if response.status < 400:
            return json.loads(response.response)
        else:
            raise Exception("Unexpected Error: %s" % response.errorDump())

    def gitlab_createmergerequest(self, variables):
        gitlab_server = Client.get_gitlab_server(variables)
        gitlab_url = Client.get_gitlab_url(gitlab_server)
        api_key =  Client.get_gitlab_api_key(gitlab_server, variables)
        content="source_branch=" + variables['source_branch'] + "&target_branch=" + variables['target_branch'] + "&title=" + variables['title']
        request = HttpRequest(variables['gitlab_server'])
        response = request.post('/api/v3/projects/' + variables['project_id'] + '/merge_requests?private_token=' + api_key, content, contentType = '')
        data = Client.handle_response(response)
        merge_id = data.get('id')
        print "Created Merge Request %s in GitLab at %s." % (merge_id, gitlab_url)
        return {"merge_id" : "%s" % merge_id}

    def gitlab_acceptmergerequest(self, variables):
        gitlab_server = Client.get_gitlab_server(variables)
        gitlab_url = Client.get_gitlab_url(gitlab_server)
        api_key =  Client.get_gitlab_api_key(gitlab_server, variables)
        request = HttpRequest(gitlab_server)
        response = request.put('/api/v3/projects/' + variables['project_id'] + '/merge_requests/' + variables['merge_id'] + '/merge?private_token=' + api_key, '', contentType = '')
        data = Client.handle_response(response)
        merge_id = data.get('id')
        print "Created Merge Request %s in GitLab at %s." % (merge_id, gitlab_url)
        return {"output" : "SUCCESS"}

