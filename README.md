[![Build Status](https://travis-ci.org/xebialabs-community/xlr-gitlab-plugin.svg?branch=master)](https://travis-ci.org/xebialabs-community/xlr-gitlab-plugin)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bf3bcce182d649eabb81183af545c80c)](https://www.codacy.com/app/erasmussen39/xlr-gitlab-plugin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xebialabs-community/xlr-gitlab-plugin&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/080f8c6a66e9d765d11e/maintainability)](https://codeclimate.com/github/xebialabs-community/xlr-gitlab-plugin/maintainability)
[![License: MIT][xlr-gitlab-plugin-license-image] ][xlr-gitlab-plugin-license-url]
[![Github All Releases][xlr-gitlab-plugin-downloads-image]]()

[xlr-gitlab-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-gitlab-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-gitlab-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-gitlab-plugin/total.svg

# Preface #
This document describes the functionality provided by the xlr-gitlab-plugin.

Please see the [XL Release Documentation](https://docs.xebialabs.com/xl-release/) for background information on XL Release and release concepts.

# Overview #
The xlr-gitlab-plugin provides the following XL Release functionality:

### Tasks ###
  * Create a merge request in GitLab.
  * Accept a merge request in GitLab.
  * Query for projects in GitLab.
  * Query for merge requests in GitLab.
  
### Webhook (Configured in Gitlab) ###
  * Commit Webhook
  * Merge Pull Request Webhook

## Shared Configuration ##
#### GitLab Server
![Server Configuration](images/shared_config.png)

  * Title : Title of GitLab server configuration.
  * Url : URL for GitLab server.
  * API Key : API key to use (configured in GitLab).

## Tasks ##
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

#### Query Project
![Create Merge Request](images/query_project.png)

  *  GitLab Server : The GitLab Server configuration to use for this task.
  *  API Key : Optional override API Key.
  *  Project Name : Name of the Project to query for.
  *  Namespace : Optional namespace to limit the query to (groups).
  *  Project ID : Numerical Project ID for GitLab Project.

#### Query Merge Requests
![Create Merge Request](images/query_merge_requests.png)

  *  GitLab Server : The GitLab Server configuration to use for this task.
  *  API Key : Optional override API Key.
  *  Project ID : Numerical Project ID for GitLab Project.
  *  Milestone : Optional milestone to query on.
  *  State : State of the Merge Requests to find (all, opened, closed, merged).
  *  Merge Requests : The list of Merge Requests discovered by the query (json).

## Webhooks ##

### Code Commit/Push Webhook ###

##### Gitlab Webhook Configuration

Here's the URL Format : 
```
http://username:password@xlrserver:port/api/extension/gitlab/commit_webhook?template=<templateName/prefix> 
```

![Gitlab Webhook Configuration](images/commit_webhook_configure.png)

##### Release Summary view in XL Release  #####
![Release Summary view in XL Release](images/commit_webhook_release.png)

##### Release Variables created #####
![Release Variables created](images/commit_webhook_variables.png)


### Merge Pull Request Webhook ###

##### Gitlab Webhook Configuration #####
```
http://username:password@xlrserver:port/api/extension/gitlab/pr_webhook?template=<templateName/prefix> 
```

![Gitlab Webhook Configuration](images/pr_webhook_configure.png)

##### Release Summary view in XL Release  #####
![Release Summary view in XL Release](images/pr_webhook_release.png)

##### Release Variables created #####
![Release Variables created](images/pr_webhook_variables.png)


