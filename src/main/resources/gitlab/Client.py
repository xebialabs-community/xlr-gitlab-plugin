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

    @staticmethod
    def get_client():
        return Client()

    @staticmethod
    def get_gitlab_server(variables):
        gitlab_server = variables["gitlab_server"]
        if gitlab_server is None:
            raise Exception("No GitLab Server provided!")
        return gitlab_server

    @staticmethod
    def get_gitlab_api_key(variables):
        gitlab_server = Client.get_gitlab_server(variables)
        if not variables["api_key"]:
            if variables["gitlab_server"]["api_key"]:
                return gitlab_server["api_key"]
            else:
                raise Exception("API Key Not Set!")
        else:
            return variables["api_key"]

    @staticmethod
    def handle_response(response):
        if response.status < 400:
            return json.loads(response.response)
        else:
            raise Exception("Unexpected Error: {}".format(response.errorDump()))

    @staticmethod
    def build_projects_endpoint(url, variables):
        return "/api/v4/projects{0}&private_token={1}".format(
            url, Client.get_gitlab_api_key(variables),
        )

    @staticmethod
    def build_projects_pipeline_endpoint(project):
        return "/api/v4/projects/{0}/trigger/pipeline".format(project)

    @staticmethod
    def build_content(params):
        content = ""
        for key in params.keys():
            value = params[key]
            if value is not None:
                content = "{0}&{1}={2}".format(content, key, value)
        return content

    @staticmethod
    def get_request(variables):
        gitlab_server = Client.get_gitlab_server(variables)
        return HttpRequest(gitlab_server)

    @staticmethod
    def gitlab_createmergerequest(variables):
        content = Client.build_content(
            {
                "source_branch": variables["source_branch"],
                "target_branch": variables["target_branch"],
                "title": variables["title"],
                "target_project_id": variables["target_project_id"],
            }
        )
        data = Client.handle_response(
            Client.get_request(variables).post(
                Client.build_projects_endpoint(
                    "/{}/merge_requests?".format(variables["project_id"]), variables
                ),
                content,
                contentType="",
            )
        )
        return {"merge_id": str(data.get("iid"))}

    @staticmethod
    def gitlab_acceptmergerequest(variables):
        Client.handle_response(
            Client.get_request(variables).put(
                Client.build_projects_endpoint(
                    "/{0}/merge_requests/{1}/merge?".format(
                        variables["project_id"], variables["merge_id"]
                    ),
                    variables,
                ),
                "",
                contentType="",
            )
        )

    @staticmethod
    def filter_project_on_namespace(data, namespace):
        if namespace is None:
            return {"project_id": ""}
        for project in data:
            if namespace in project["name_with_namespace"]:
                return {"project_id": str(project["id"])}
        return {"project_id": ""}

    @staticmethod
    def gitlab_querydata(variables):
        data = Client.handle_response(
            Client.get_request(variables).get(
                "{0}?private_token={1}".format(
                    variables["endpoint"], Client.get_gitlab_api_key(variables),
                )
            )
        )
        jsoncontext = JsonPath.parse(data)
        return {"value": str(jsoncontext.read(variables["path_spec"]))}

    @staticmethod
    def gitlab_querysecuredata(variables):
        # The returned value is handled as a password in the XLR user interface, but the API call is the same as gitlab_querydata
        return Client.gitlab_querydata(variables)

    @staticmethod
    def gitlab_queryproject(variables):
        data = Client.handle_response(
            Client.get_request(variables).get(
                Client.build_projects_endpoint(
                    "?search={}".format(variables["project_name"]), variables
                )
            )
        )
        if len(data) == 1:
            return {"project_id": str(data[0]["id"])}
        elif len(data) > 1:
            return Client.filter_project_on_namespace(data, variables["namespace"])

    @staticmethod
    def gitlab_querymergerequests(variables):
        endpoint = Client.build_projects_endpoint(
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
            response = Client.get_request(variables).get(endpoint_page)
            merge_requests_set = Client.handle_response(response)
            if merge_requests_set == []:  # no more results to pull
                break
            else:  # pull results based on expected results_limit count for that page
                merge_requests += merge_requests_set[0:result_set_size]
        return {"merge_requests": str(json.dumps(merge_requests))}

    @staticmethod
    def gitlab_createtag(variables):
        content = Client.build_content(
            {
                "tag_name": variables["tag_name"],
                "ref": variables["ref"],
                "message": variables["message"],
            }
        )
        data = Client.handle_response(
            Client.get_request(variables).post(
                Client.build_projects_endpoint(
                    "/{}/repository/tags?".format(variables["project_id"]), variables
                ),
                content,
                contentType="",
            )
        )
        return {"commit_id": str(data["commit"]["id"])}

    @staticmethod
    def gitlab_createbranch(variables):
        content = Client.build_content(
            {"branch": variables["branch"], "ref": variables["ref"]}
        )
        data = Client.handle_response(
            Client.get_request(variables).post(
                Client.build_projects_endpoint(
                    "/{}/repository/branches?".format(variables["project_id"]),
                    variables,
                ),
                content,
                contentType="",
            )
        )
        return {"commit_id": str(data["commit"]["id"])}

    @staticmethod
    def gitlab_triggerpipeline(variables):
        endpoint = "/api/v4/projects/{0}/ref/{1}/trigger/pipeline?token={2}".format(
            variables["project_id"], variables["ref"], variables["token"]
        )
        for key, value in variables["variables"].iteritems():
            endpoint += "&variables[{0}]={1}".format(key, value)

        print "* gitlab_triggerpipeline.endpoint: {0}".format(endpoint)
        data = Client.handle_response(
            Client.get_request(variables).post(endpoint, "", contentType="")
        )
        print "[Pipeline #{0}]({1})".format(data["id"], data["web_url"])
        status = {"pipeline_id": str(data["id"]), "status": str(data["status"])}
        return status

    @staticmethod
    def gitlab_pipeline_status(variables):
        pipeline_id = variables["pipeline_id"]
        endpoint = "/api/v4/projects/{0}/pipelines/{1}?private_token={2}".format(
            variables["project_id"], pipeline_id, Client.get_gitlab_api_key(variables)
        )
        data = Client.handle_response(Client.get_request(variables).get(endpoint))
        status = {
            "pipeline_id": "{0}".format(data.get("id")),
            "status": data.get("status"),
            "web_url": data.get("web_url"),
        }
        return status

    @staticmethod
    def gitlab_branch_statuses(variables):
        endpoint = "/api/v4/projects/{0}/repository/branches?private_token={1}".format(
            variables["project_id"], Client.get_gitlab_api_key(variables)
        )
        branches = Client.handle_response(Client.get_request(variables).get(endpoint))
        # build a map of the commit ids for each branch
        latest_commits = {}
        for branch in branches:
            if not variables["branchName"] or branch["name"] == variables["branchName"]:
                branch_id = branch["name"]
                last_commit = branch["commit"]["id"]
                latest_commits[branch_id] = last_commit
        return latest_commits

    @staticmethod
    def gitlab_tag_statuses(variables):
        endpoint = "/api/v4/projects/{0}/repository/tags?private_token={1}&order_by=updated&sort=asc".format(
            variables["project_id"], Client.get_gitlab_api_key(variables)
        )
        if variables["search"] not in [None, ""]:
            endpoint += "&search={0}".format(variables["search"])
        return Client.handle_response(Client.get_request(variables).get(endpoint))

    @staticmethod
    def gitlab_createproject(variables):
        proj_spec = {
            "name": variables["project_name"],
            "path": variables["path"],
            "visibility": variables["visibility"],
        }
        for optional_spec in ["namespace", "description", "import_url"]:
            if optional_spec in variables.keys():
                api_attribute = (
                    "namespace_id" if optional_spec == "namespace" else optional_spec
                )
                proj_spec[api_attribute] = variables[optional_spec]
        content = Client.build_content(proj_spec)
        endpoint = "/api/v4/projects?private_token={0}".format(
            Client.get_gitlab_api_key(variables)
        )
        data = Client.handle_response(
            Client.get_request(variables).post(endpoint, content, contentType="")
        )
        return {"project_id": str(data["id"])}

    @staticmethod
    def gitlab_creategroup(variables):
        group_spec = {
            "name": variables["group_name"],
            "path": variables["path"],
            "visibility": variables["visibility"],
        }
        for optional_spec in ["description"]:
            if optional_spec in variables.keys():
                group_spec[optional_spec] = variables[optional_spec]
        content = Client.build_content(group_spec)
        endpoint = "/api/v4/groups?private_token={0}".format(
            Client.get_gitlab_api_key(variables)
        )
        data = Client.handle_response(
            Client.get_request(variables).post(endpoint, content, contentType="")
        )
        return {"group_id": str(data["id"])}

    @staticmethod
    def gitlab_querycommits(variables):
        endpoint = "/api/v4/projects/{0}/repository/commits?private_token={1}".format(
            variables["project_id"], Client.get_gitlab_api_key(variables)
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
            response = Client.get_request(variables).get(endpoint_page)
            commits_set = Client.handle_response(response)
            if commits_set == []:  # no more results to pull
                break
            else:  # pull results based on expected results_limit count for that page
                commits += commits_set[0:result_set_size]
        return {"commits": str(json.dumps(commits))}

    @staticmethod
    def gitlab_querytags(variables):
        endpoint = "/api/v4/projects/{0}/repository/tags?private_token={1}&order_by=updated&sort=asc".format(
            variables["project_id"], Client.get_gitlab_api_key(variables)
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
            response = Client.get_request(variables).get(endpoint_page)
            tags_set = Client.handle_response(response)
            if tags_set == []:  # no more results to pull
                break
            else:  # pull results based on expected results_limit count for that page
                tags += tags_set[0:result_set_size]
        return {"tags": str(json.dumps(tags))}

    @staticmethod
    def gitlab_querypipelines(variables):
        endpoint = "/api/v4/projects/{0}/pipelines?private_token={1}".format(
            variables["project_id"], Client.get_gitlab_api_key(variables)
        )
        data = Client.handle_response(Client.get_request(variables).get(endpoint))
        return {"pipelines": str(json.dumps(data))}

    @staticmethod
    def gitlab_createprojectwebhook(variables):
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
        content = Client.build_content(webhook)
        data = Client.handle_response(
            Client.get_request(variables).post(
                Client.build_projects_endpoint(
                    "/{}/hooks?".format(variables["project_id"]), variables
                ),
                content,
                contentType="",
            )
        )
        return {"hook_id": str(data["id"])}
