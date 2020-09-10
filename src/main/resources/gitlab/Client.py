#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
from xlrelease.HttpRequest import HttpRequest
from com.jayway.jsonpath import JsonPath

PAGE_SIZE = 100


class Client(object):
    def __init__(self):
        return

    def get_client(self):
        return Client()

    def get_gitlab_server(self, variables):
        gitlab_server = variables["gitlab_server"]
        if gitlab_server is None:
            raise Exception("No GitLab Server provided!")
        return gitlab_server

    def get_gitlab_api_key(self, variables):
        gitlab_server = self.get_gitlab_server(variables)
        if not variables["api_key"]:
            if variables["gitlab_server"]["api_key"]:
                return gitlab_server["api_key"]
            else:
                raise Exception("API Key Not Set!")
        else:
            return variables["api_key"]

    def handle_response(self, response):
        if response.status < 400:
            return json.loads(response.response)
        else:
            raise Exception("Unexpected Error: {}".format(response.errorDump()))

    def build_projects_endpoint(self, url, variables):
        return "/api/v4/projects{0}&private_token={1}".format(
            url, self.get_gitlab_api_key(variables),
        )

    def build_projects_pipeline_endpoint(self, project):
        return "/api/v4/projects/{0}/trigger/pipeline".format(project)

    def build_content(self, params):
        content = ""
        for key in params.keys():
            value = params[key]
            if value is not None:
                content = "{0}&{1}={2}".format(content, key, value)
        return content

    def get_request(self, variables):
        gitlab_server = self.get_gitlab_server(variables)
        return HttpRequest(gitlab_server)

    def gitlab_createmergerequest(self, variables):
        content ={ "source_branch": variables["source_branch"], "target_branch": variables["target_branch"],
            "title": variables["title"], "target_project_id": variables["target_project_id"]}
        content = json.dumps(content)
        data = self.handle_response(
            self.get_request(variables).post(
                self.build_projects_endpoint(
                    "/{}/merge_requests?".format(variables["project_id"]), variables
                ),
                content,
                contentType="application/json",
            )
        )
        return {"merge_id": str(data.get("iid"))}

    def gitlab_acceptmergerequest(self, variables):
        self.handle_response(
            self.get_request(variables).put(
                self.build_projects_endpoint(
                    "/{0}/merge_requests/{1}/merge?".format(
                        variables["project_id"], variables["merge_id"]
                    ),
                    variables,
                ),
                "",
                contentType="",
            )
        )

    def filter_project_on_namespace(self, data, namespace):
        if namespace is None:
            return {"project_id": ""}
        for project in data:
            if namespace in project["name_with_namespace"]:
                return {"project_id": str(project["id"])}
        return {"project_id": ""}

    def gitlab_querydata(self, variables):
        data = self.handle_response(
            self.get_request(variables).get(
                "{0}?private_token={1}".format(
                    variables["endpoint"], self.get_gitlab_api_key(variables),
                ), contentType="application/json"
            )
        )
        jsoncontext = JsonPath.parse(data)
        return {"value": str(jsoncontext.read(variables["path_spec"]))}

    def gitlab_querysecuredata(self, variables):
        # The returned value is handled as a password in the XLR user interface, but the API call is the same as gitlab_querydata
        return self.gitlab_querydata(variables)

    def gitlab_queryproject(self, variables):
        data = self.handle_response(
            self.get_request(variables).get(
                self.build_projects_endpoint(
                    "?search={}".format(variables["project_name"]), variables
                ), contentType="application/json"
            )
        )
        if len(data) == 1:
            return {"project_id": str(data[0]["id"])}
        elif len(data) > 1:
            return self.filter_project_on_namespace(data, variables["namespace"])

    def gitlab_querymergerequests(self, variables):
        endpoint = self.build_projects_endpoint(
            "/{0}/merge_requests?state={1}".format(
                variables["project_id"], variables["state"]
            ),
            variables,
        )
        # Sorting and filtering merge request results
        if variables["sorting"] == "Creation Datetime Descending":
            endpoint += "&order_by=created_at&sort=desc"
        if variables["sorting"] == "Creation Datetime Ascending":
            endpoint += "&order_by=created_at&sort=asc"
        if variables["sorting"] == "Last Update Datetime Descending":
            endpoint += "&order_by=updated_at&sort=desc"
        if variables["sorting"] == "Last Update Datetime Ascending":
            endpoint += "&order_by=updated_at&sort=asc"
        if variables["simple_view"]:
            endpoint += "&view=simple"
        if variables["source_branch"] is not None:
            endpoint += "&source_branch={}".format(variables["source_branch"])
        if variables["target_branch"] is not None:
            endpoint += "&target_branch={}".format(variables["target_branch"])
        if variables["milestone"] is not None:
            endpoint += "&milestone={}".format(variables["milestone"])
        # Pagination
        merge_requests = []
        # Calculate page sizes using max PAGE_SIZE results per page (GitLab limit) and the user-specified results_limit
        result_set_sizes = [
            min(variables["results_limit"] - i, PAGE_SIZE)
            for i in range(0, variables["results_limit"], PAGE_SIZE)
        ]
        for page_num, result_set_size in enumerate(result_set_sizes, 1):
            endpoint_page = endpoint + "&per_page={0}&page={1}".format(
                PAGE_SIZE, page_num
            )
            response = self.get_request(variables).get(endpoint_page, contentType="application/json")
            merge_requests_set = self.handle_response(response)
            if merge_requests_set == []:  # no more results to pull
                break
            else:  # pull results based on expected results_limit count for that page
                merge_requests += merge_requests_set[0:result_set_size]
        return {"merge_requests": str(json.dumps(merge_requests))}

    def gitlab_createtag(self, variables):
        content = {
            "tag_name": variables["tag_name"],
            "ref": variables["ref"],
            "message": variables["message"]
        }
        content = json.dumps(content)
        data = self.handle_response(
            self.get_request(variables).post(
                self.build_projects_endpoint(
                    "/{}/repository/tags?".format(variables["project_id"]), variables
                ),
                content,
                contentType="application/json",
            )
        )
        return {"commit_id": str(data["commit"]["id"])}

    def gitlab_createbranch(self, variables):
        content = {"branch": variables["branch"], "ref": variables["ref"]}
        content = json.dumps(content)
        data = self.handle_response(
            self.get_request(variables).post(
                self.build_projects_endpoint(
                    "/{}/repository/branches?".format(variables["project_id"]),
                    variables,
                ),
                content,
                contentType="application/json",
            )
        )
        return {"commit_id": str(data["commit"]["id"])}

    def gitlab_triggerpipeline(self, variables):
        endpoint = "/api/v4/projects/{0}/ref/{1}/trigger/pipeline?token={2}".format(
            variables["project_id"], variables["ref"], variables["token"]
        )
        for key, value in variables["variables"].iteritems():
            endpoint += "&variables[{0}]={1}".format(key, value)

        print "* gitlab_triggerpipeline.endpoint: {0}".format(endpoint)
        data = self.handle_response(
            self.get_request(variables).post(endpoint, "", contentType="application/json")
        )
        print "[Pipeline #{0}]({1})".format(data["id"], data["web_url"])
        status = {"pipeline_id": str(data["id"]), "status": str(data["status"])}
        return status

    def gitlab_pipeline_status(self, variables):
        pipeline_id = variables["pipeline_id"]
        endpoint = "/api/v4/projects/{0}/pipelines/{1}?private_token={2}".format(
            variables["project_id"], pipeline_id, self.get_gitlab_api_key(variables)
        )
        data = self.handle_response(self.get_request(variables).get(endpoint, contentType="application/json"
        ))
        status = {
            "pipeline_id": "{0}".format(data.get("id")),
            "status": data.get("status"),
            "web_url": data.get("web_url"),
        }
        return status

    def gitlab_branch_statuses(self, variables):
        endpoint = "/api/v4/projects/{0}/repository/branches?private_token={1}".format(
            variables["project_id"], self.get_gitlab_api_key(variables)
        )
        branches = self.handle_response(self.get_request(variables).get(endpoint, contentType="application/json"))
        # build a map of the commit ids for each branch
        latest_commits = {}
        for branch in branches:
            if not variables["branchName"] or branch["name"] == variables["branchName"]:
                branch_id = branch["name"]
                last_commit = branch["commit"]["id"]
                latest_commits[branch_id] = last_commit
        return latest_commits

    def gitlab_tag_statuses(self, variables):
        endpoint = "/api/v4/projects/{0}/repository/tags?private_token={1}&order_by=updated&sort=desc".format(
            variables["project_id"], self.get_gitlab_api_key(variables)
        )
        if variables["search"] not in [None, ""]:
            endpoint += "&search={0}".format(variables["search"])
        return self.handle_response(self.get_request(variables).get(endpoint, contentType="application/json"))

    def gitlab_createproject(self, variables):
        proj_spec = {
            "name": variables["project_name"],
            "path": variables["path"],
            "visibility": variables["visibility"]
        }
        for optional_spec in ["namespace", "description", "import_url"]:
            if optional_spec in variables.keys():
                api_attribute = (
                    "namespace_id" if optional_spec == "namespace" else optional_spec
                )
                proj_spec[api_attribute] = variables[optional_spec]
        endpoint = "/api/v4/projects?private_token={0}".format(
            self.get_gitlab_api_key(variables)
        )
        content = json.dumps(proj_spec)
        data = self.handle_response(
            self.get_request(variables).post(endpoint, content, contentType="application/json")
        )
        return {"project_id": str(data["id"])}

    def gitlab_creategroup(self, variables):
        group_spec = {
            "name": variables["group_name"],
            "path": variables["path"],
            "visibility": variables["visibility"],
        }
        for optional_spec in ["description", "parent_id"]:
            if optional_spec in variables.keys():
                group_spec[optional_spec] = variables[optional_spec]
        # content = Client.build_content(group_spec)
        content = json.dumps(proj_spec)
        endpoint = "/api/v4/groups?private_token={0}".format(
            self.get_gitlab_api_key(variables)
        )
        data = self.handle_response(
            self.get_request(variables).post(endpoint, content, contentType="application/json")
        )
        return {"group_id": str(data["id"])}

    def gitlab_querycommits(self, variables):
        endpoint = "/api/v4/projects/{0}/repository/commits?private_token={1}".format(
            variables["project_id"], self.get_gitlab_api_key(variables)
        )
        if variables["branch"] is not None:
            endpoint += "&" + "ref_name=" + variables["branch"]
        # Pagination
        commits = []
        # Calculate page sizes using max PAGE_SIZE results per page (GitLab limit) and the user-specified results_limit
        result_set_sizes = [
            min(variables["results_limit"] - i, PAGE_SIZE)
            for i in range(0, variables["results_limit"], PAGE_SIZE)
        ]
        for page_num, result_set_size in enumerate(result_set_sizes, 1):
            endpoint_page = endpoint + "&per_page={0}&page={1}".format(
                PAGE_SIZE, page_num
            )
            response = self.get_request(variables).get(endpoint_page, contentType="application/json")
            commits_set = self.handle_response(response)
            if commits_set == []:  # no more results to pull
                break
            else:  # pull results based on expected results_limit count for that page
                commits += commits_set[0:result_set_size]
        return {"commits": str(json.dumps(commits))}

    def gitlab_querytags(self, variables):
        endpoint = "/api/v4/projects/{0}/repository/tags?private_token={1}&order_by=updated&sort=asc".format(
            variables["project_id"], self.get_gitlab_api_key(variables)
        )
        if variables["search"] not in [None, ""]:
            endpoint += "&search={0}".format(variables["search"])
        # Pagination
        tags = []
        # Calculate page sizes using max PAGE_SIZE results per page (GitLab limit) and the user-specified results_limit
        result_set_sizes = [
            min(variables["results_limit"] - i, PAGE_SIZE)
            for i in range(0, variables["results_limit"], PAGE_SIZE)
        ]
        for page_num, result_set_size in enumerate(result_set_sizes, 1):
            endpoint_page = endpoint + "&per_page={0}&page={1}".format(
                PAGE_SIZE, page_num
            )
            response = self.get_request(variables).get(endpoint_page, contentType="application/json")
            tags_set = self.handle_response(response)
            if tags_set == []:  # no more results to pull
                break
            else:  # pull results based on expected results_limit count for that page
                tags += tags_set[0:result_set_size]
        return {"tags": str(json.dumps(tags))}

    def gitlab_querypipelines(self, variables):
        endpoint = "/api/v4/projects/{0}/pipelines?private_token={1}".format(
            variables["project_id"], self.get_gitlab_api_key(variables)
        )
        data = self.handle_response(self.get_request(variables).get(endpoint, contentType="application/json"))
        return {"pipelines": str(json.dumps(data))}

    def gitlab_createprojectwebhook(self, variables):
        content_params = [
            "url",
            "push_events",
            "issues_events",
            "confidential_issues_events",
            "merge_requests_events",
            "tag_push_events",
            "note_events",
            "job_events",
            "pipeline_events",
            "wiki_page_events",
            "enable_ssl_verification",
            "token",
        ]
        webhook = {}
        for var_key in variables.keys():
            if var_key in content_params:
                webhook[var_key] = variables[var_key]
        content = json.dumps(webhook)
        data = self.handle_response(
            self.get_request(variables).post(
                self.build_projects_endpoint(
                    "/{}/hooks?".format(variables["project_id"]), variables
                ),
                content,
                contentType="application/json",
            )
        )
        return {"hook_id": str(data["id"])}
