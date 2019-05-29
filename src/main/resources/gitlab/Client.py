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
    def get_gitlab_api_key(variables):
        gitlab_server = Client.get_gitlab_server(variables)
        if not variables['api_key']:
            if variables['gitlab_server']['api_key']:
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

    @staticmethod
    def build_projects_endpoint(url, variables):
        return "/api/v4/projects%s&private_token=%s" % (url, Client.get_gitlab_api_key(variables))

    @staticmethod
    def build_content(params):
        content = ""
        for key in params.keys():
            value = params[key]
            if value is not None:
                content = "%s&%s=%s" % (content, key, value)
        return content

    @staticmethod
    def get_request(variables):
        gitlab_server = Client.get_gitlab_server(variables)
        return HttpRequest(gitlab_server)

    @staticmethod
    def gitlab_createmergerequest(variables):
        content = Client.build_content({"source_branch" : variables['source_branch'], "target_branch" : variables['target_branch'], "title" : variables['title'], "target_project_id" : variables['target_project_id']})
        data = Client.handle_response(Client.get_request(variables).post(
            Client.build_projects_endpoint("/%s/merge_requests?" % variables['project_id'], variables),
            content,
            contentType = ''))
        return {"merge_id" : "%s" % data.get('iid')}

    @staticmethod
    def gitlab_acceptmergerequest(variables):
        Client.handle_response(Client.get_request(variables).put(
            Client.build_projects_endpoint("/%s/merge_requests/%s/merge?" % (variables['project_id'], variables['merge_id']), variables), '', contentType = ''))

    @staticmethod
    def filter_project_on_namespace(data, namespace):
        if namespace is None:
            return {"project_id" : ""}
        for project in data:
            if namespace in project['name_with_namespace']:
                return {"project_id" : "%s" % project['id']}
        return {"project_id" : ""}

    @staticmethod
    def gitlab_queryproject(variables):
        data = Client.handle_response(Client.get_request(variables).get(
            Client.build_projects_endpoint("?search=%s" % variables['project_name'], variables)))
        if len(data) == 1:
            return {"project_id" : "%s" % data[0]['id']}
        elif len(data) > 1:
            return Client.filter_project_on_namespace(data, variables['namespace'])

    @staticmethod
    def gitlab_querymergerequests(variables):
        endpoint = Client.build_projects_endpoint("/%s/merge_requests?state=%s" % (variables['project_id'], variables['state']), variables)
        # Sorting and filtering merge request results
        if variables['sorting'] == 'Creation Datetime Descending':
            endpoint = "%s&order_by=created_at&sort=desc" % endpoint
        if variables['sorting'] == 'Creation Datetime Ascending':
            endpoint = "%s&order_by=created_at&sort=asc" % endpoint
        if variables['sorting'] == 'Last Update Datetime Descending':
            endpoint = "%s&order_by=updated_at&sort=desc" % endpoint
        if variables['sorting'] == 'Last Update Datetime Ascending':
            endpoint = "%s&order_by=updated_at&sort=asc" % endpoint
        if variables['simple_view']:
            endpoint = "%s&view=simple" % endpoint
        if variables['source_branch'] is not None:
            endpoint = "%s&source_branch=%s" % (endpoint, variables['source_branch'])
        if variables['target_branch'] is not None:
            endpoint = "%s&target_branch=%s" % (endpoint, variables['target_branch'])
        if variables['milestone'] is not None:
            endpoint = "%s&milestone=%s" % (endpoint, variables['milestone'])
        # Pagination
        merge_requests = []
        # Calculate page sizes using max 100 results per page (GitLab limit) and the user-specified results_limit
        result_set_sizes = [min(variables['results_limit']-i,100) for i in range(0, variables['results_limit'], 100)]
        for page_num, result_set_size in enumerate(result_set_sizes, 1):
            endpoint_page = "%s&per_page=100&page=%s" % (endpoint, page_num)
            response = Client.get_request(variables).get(endpoint_page)
            merge_requests_set = Client.handle_response(response)
            if merge_requests_set == []:  # no more results to pull
                break
            else:  # pull results based on expected results_limit count for that page
                merge_requests += merge_requests_set[0:result_set_size]
        return {"merge_requests" : "%s" % merge_requests}

    @staticmethod
    def gitlab_createtag(variables):
        content = Client.build_content({"tag_name" : variables['tag_name'], "ref" : variables['ref'], "message" : variables['message']})
        data = Client.handle_response(Client.get_request(variables).post(
            Client.build_projects_endpoint("/%s/repository/tags?" % variables['project_id'], variables),
            content,
            contentType = ''))
        return {"commit_id" : "%s" % data.get('commit').get('id')}

    @staticmethod
    def gitlab_createbranch(variables):
        content = Client.build_content({"branch" : variables['branch'], "ref" : variables['ref']})
        data = Client.handle_response(Client.get_request(variables).post(
            Client.build_projects_endpoint("/%s/repository/branches?" % variables['project_id'], variables),
            content,
            contentType = ''))
        return {"commit_id" : "%s" % data['commit']['id']}
