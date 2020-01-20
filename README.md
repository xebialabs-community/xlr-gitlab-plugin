[![Build Status](https://travis-ci.org/xebialabs-community/xlr-gitlab-plugin.svg?branch=master)](https://travis-ci.org/xebialabs-community/xlr-gitlab-plugin)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bf3bcce182d649eabb81183af545c80c)](https://www.codacy.com/app/erasmussen39/xlr-gitlab-plugin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xebialabs-community/xlr-gitlab-plugin&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/080f8c6a66e9d765d11e/maintainability)](https://codeclimate.com/github/xebialabs-community/xlr-gitlab-plugin/maintainability)
[![License: MIT][xlr-gitlab-plugin-license-image] ][xlr-gitlab-plugin-license-url]
[![Github All Releases][xlr-gitlab-plugin-downloads-image]]()

[xlr-gitlab-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-gitlab-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-gitlab-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-gitlab-plugin/total.svg

# Preface
This document describes the functionality provided by the xlr-gitlab-plugin.

Please see the [XL Release Documentation](https://docs.xebialabs.com/xl-release/) for background information on XL Release and release concepts.

# Overview
The xlr-gitlab-plugin provides the following XL Release functionality:

### Tasks
  * Query for merge requests
  * Create a merge request
  * Accept a merge request
  * Create a tag
  * Create a branch
  * Query for projects
  * Create a project
  * Create a project webhook
  * Create a group
  * Trigger a pipeline
  * Query Data
  * Query Secure Data

### Triggers
  * Commit Trigger

### Webhook (Configured in Gitlab)
  * Commit Webhook
  * Merge Pull Request Webhook

## Shared Configuration
#### GitLab Server
![Server Configuration](images/shared_config.png)

  * Title : Title of GitLab server configuration.
  * Url : URL for GitLab server.
  * API Key : API key to use (configured in GitLab).

## Tasks
#### Create Merge Request
![Create Merge Request](images/create_merge_request.png)

  *  GitLab Server : The GitLab Server configuration to use for this task.
  *  API Key : Optional override API Key.
  *  Project ID : Numerical Project ID for GitLab Project.
  *  Source Branch : Source branch for the merge request.
  *  Target Branch : Target branch for the merge request.
  *  Merge Title : Title for the merge request.
  *  Target Project ID : Numerical Target Project ID for the target GitLab Project (forked repos).
  *  Merge ID : Merge ID of the newly created merge request returned from GitLab.

#### Accept Merge Request
![Create Merge Request](images/accept_merge_request.png)

  *  GitLab Server : The GitLab Server configuration to use for this task.
  *  API Key : Optional override API Key.
  *  Project ID : Numerical Project ID for GitLab Project.
  *  Merge ID : Numerical Merge ID for the GitLab Merge Request.

#### Query Merge Requests
![Create Merge Request](images/query_merge_requests.png)

  *  GitLab Server : The GitLab Server configuration to use for this task.
  *  API Key : Optional override API Key.
  *  Project ID : Numerical Project ID for GitLab Project.
  *  Milestone : Optional milestone to query on.
  *  State : State of the Merge Requests to find (all, opened, closed, merged).
  *  Merge Requests : The list of Merge Requests discovered by the query (json).

#### Create Branch
![Create Branch](images/create_branch.png)

  *  GitLab Server : The GitLab Server configuration to use for this task.
  *  API Key : Optional override API Key.
  *  Project ID : Numerical Project ID for GitLab Project.
  *  New Branch Name : The name of the branch to be created.
  *  Ref : Commit SHA or existing branch name to create the new branch from.

#### Create Tag
![Create Tag](images/create_tag.png)

  *  GitLab Server : The GitLab Server configuration to use for this task.
  *  API Key : Optional override API Key.
  *  Project ID : Numerical Project ID for GitLab Project.
  *  Ref : Commit SHA, another tag name, or branch name to create the tag from.
  *  Tag Name : The name of the tag.
  *  Tag Message : An optional description for the tag.
  *  Commit ID : The ID of the commit used by the newly created tag (useful when specifying a branch or tag name as Ref).

#### Query Project
![Query Project](images/query_project.png)

  *  GitLab Server : The GitLab Server configuration to use for this task.
  *  API Key : Optional override API Key.
  *  Project Name : Name of the Project to query for.
  *  Namespace : Optional namespace to limit the query to (groups).
  *  Project ID : Numerical Project ID for GitLab Project.

#### Create Project
![Create Project](images/create_project.png)

  *  GitLab Server : The GitLab Server configuration to use for this task.
  *  API Key : Optionally, override the API Key.
  *  Project Name : Name of the Project to create.
  *  Path : Path for the Project to create.
  *  Namespace : Namespace (could be a user or a group) ID for the project.
  *  Description : Optionally, provide a project description.
  *  Import URL : Optionally, provide an import URL to import a different repo.
  *  Visibility : Visibility of the project - private, internal, or public.
  *  Project ID : Project ID of the create GitLab Project (this is an output property).

#### Create Project Webhook
![Create Project Webhook](images/create_project_webhook.png)

  *  GitLab Server : The GitLab Server configuration to use for this task.
  *  API Key : Optionally, override the API Key.
  *  Project ID : ID of the project to add a webhook to.
  *  Triggers : A variety of boolean properties to configure on which events the webhook will trigger.
  *  Hook ID : Webhook ID after creation (this is an output property).

#### Create Group
![Create Group](images/create_group.png)

  *  GitLab Server : The GitLab Server configuration to use for this task.
  *  API Key : Optionally, override the API Key.
  *  Group Name : Name of the new group.
  *  Path : Path for the new group.
  *  Description : Optionally, provide a group description.
  *  Visibility : Visibility of the group - private, internal, or public.
  *  Group ID : Group ID of the new GitLab group (this is an output property).

#### Trigger Pipeline
![Trigger Pipeline](images/trigger_pipeline.png)

#### Query Data
This task enables pulling a text value from any GET method Gitlab API endpoint.  A JSON path expression should be supplied, to identify the value of interest.

![Query Data](images/query_data.png)

#### Query Secure Data
This task enables pulling a secret value from any GET method Gitlab API endpoint.  A JSON path expression should be supplied, to identify the value of interest.  This task is the same as Query Data, except the output value is saved as a XL Release password variable.

![Query Data](images/query_secure_data.png)

## Webhooks

### Code Commit/Push Webhook

##### Gitlab Webhook Configuration

Here's the URL Format :
```
http://username:password@xlrserver:port/api/extension/gitlab/commit_webhook?template=<templateName/prefix>
```

![Gitlab Webhook Configuration](images/commit_webhook_configure.png)

##### Release Summary view in XL Release
![Release Summary view in XL Release](images/commit_webhook_release.png)

##### Release Variables created
![Release Variables created](images/commit_webhook_variables.png)


### Merge Pull Request Webhook

##### Gitlab Webhook Configuration
```
http://username:password@xlrserver:port/api/extension/gitlab/pr_webhook?template=<templateName/prefix>
```

![Gitlab Webhook Configuration](images/pr_webhook_configure.png)

##### Release Summary view in XL Release
![Release Summary view in XL Release](images/pr_webhook_release.png)

##### Release Variables created
![Release Variables created](images/pr_webhook_variables.png)


## Dashboard Tiles

Dashboard tiles are included in this plugin, to visualize commit, merge request, and pipelines information.  These tiles use the existing XL Release GitLab server configuration/connection and can be configured using the (usual dashboard setup approach)[https://docs.xebialabs.com/v.9.0/xl-release/get-started?subject=dashboards].  These dashboard titles are available for all dashboard scopes - release, folder, and global.

## Contributing

Please review the contributing guidelines for _xebialabs-community_ at [http://xebialabs-community.github.io/](http://xebialabs-community.github.io/)

## License

This community plugin is licensed under the [MIT license][xlr-gitlab-plugin-license-url].

See license in [LICENSE.md](LICENSE.md)

