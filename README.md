
# GitLab Integration for XL Release

[![Build Status](https://travis-ci.org/xebialabs-community/xlr-gitlab-plugin.svg?branch=master)](https://travis-ci.org/xebialabs-community/xlr-gitlab-plugin)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bf3bcce182d649eabb81183af545c80c)](https://www.codacy.com/app/erasmussen39/xlr-gitlab-plugin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xebialabs-community/xlr-gitlab-plugin&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/080f8c6a66e9d765d11e/maintainability)](https://codeclimate.com/github/xebialabs-community/xlr-gitlab-plugin/maintainability)
[![License: MIT][xlr-gitlab-plugin-license-image] ][xlr-gitlab-plugin-license-url]
[![Github All Releases][xlr-gitlab-plugin-downloads-image]]()

[xlr-gitlab-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-gitlab-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-gitlab-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-gitlab-plugin/total.svg

## Preface
This document describes the functionality provided by the xlr-gitlab-plugin.

Please see the [XL Release Documentation](https://docs.xebialabs.com/xl-release/) for background information on XL Release and release concepts.

## Installation

### Requirements

1. XL Release 9.0+

### Building the plugin
The gradle wrapper facilitates building the plugin.  Use the following command to build using [Gradle](https://gradle.org/):
```bash
./gradlew clean build
```
The built plugin, along with other files from the build, can then be found in the _build_ folder.

### Adding the plugin to XL Release

Download the latest version of the plugin from the [releases page](https://github.com/xebialabs-community/xlr-qualys-plugin/releases).  The plugin can then be installed through the XL Release graphical interface or the server backend.  For additional detail, please refer to [the docs.xebialabs.com documentation on XLR plugin installation](https://docs.xebialabs.com/xl-release/how-to/install-or-remove-xl-release-plugins.html)

## Usage

__Available Tasks__: Accept Merge Request, Create Branch, Create Group, Create Merge Request, Create Project, Create Project Webhook, Create Tag, Query Commits, Query Data, Query Merge Requests, Query Pipelines, Query Project, Query Secure Data, Query Tags, Trigger Pipeline

__Available Triggers__: Commit Trigger, Tag Trigger

__Available Dashboard Tiles__: Commits Tile, Contributions Tile, Merge Requests Tile, Pipelines Tile, Tags Timeline Tile, Timeline Tile

### Configuration
![Server Configuration](images/shared_config.png)

### Tasks

#### Accept Merge Request
Properties:
* _input_ GitLab Server 
* _input_ API Key (Optionally, override the GitLab Server configuration API token)
* _input_ Project ID (This is visible in the GUI and should be an integer)
* _input_ Merge ID (This is visible in the GUI and should be an integer)

![Accept Merge Request](images/accept_merge_request.png)

#### Create Branch
Properties:
* _input_ GitLab Server 
* _input_ API Key (Optionally, override the GitLab Server configuration API token)
* _input_ Project ID (This is visible in the GUI and should be an integer)
* _input_ New Branch Name 
* _input_ Reference (Branch name or commit hash to the create branch from)
* _output_ Commit Source (Commit hash used to generate the new branch)

![Create Branch](images/create_branch.png)

#### Create Group
Properties:
* _input_ GitLab Server 
* _input_ API Key (Optionally, override the GitLab Server configuration API token)
* _input_ Group Name 
* _input_ Group Path 
* _input_ Group Description 
* _input_ Group Visibility 
* _output_ Group ID 

![Create Group](images/create_group.png)

#### Create Merge Request
Properties:
* _input_ GitLab Server 
* _input_ API Key (Optionally, override the GitLab Server configuration API token)
* _input_ Project ID (This is visible in the GUI and should be an integer)
* _input_ Source Branch 
* _input_ Target Branch 
* _input_ Merge Request Title 
* _input_ Target Project ID 
* _output_ Merge Request ID 

![Create Merge Request](images/create_merge_request.png)

#### Create Project
Properties:
* _input_ GitLab Server 
* _input_ API Key (Optionally, override the GitLab Server configuration API token)
* _input_ Project Name 
* _input_ Project Path 
* _input_ Namespace (Namespace ID for the project.  This will default to the configuration user namespace if not provided)
* _input_ Project Description 
* _input_ Import URL (Note: If your HTTP repository is not publicly accessible, then add authentication information to the URL (e.g. https://username:password@gitlab.company.com/group/project.git))
* _input_ Project Visibility 
* _output_ Project ID 

![Create Project](images/create_project.png)

#### Create Project Webhook
Properties:
* _input_ GitLab Server 
* _input_ API Key (Optionally, override the GitLab Server configuration API token)
* _input_ Project ID (This is visible in the GUI and should be an integer)
* _input_ URL (The webhook URL)
* _input_ Push Events (Trigger hook on push events)
* _input_ Issues Events (Trigger hook on issues events)
* _input_ Confidential Issues Events (Trigger hook on confidential issues events)
* _input_ Merge Requests Events (Trigger hook on merge requests events)
* _input_ Tag Push Events (Trigger hook on tag push events)
* _input_ Note Events (Trigger hook on note events)
* _input_ Job Events (Trigger hook on job events)
* _input_ Pipeline Events (Trigger hook on pipeline events)
* _input_ Wiki Page Events (Trigger hook on wiki events)
* _input_ Verify SSL (Do SSL verification when triggering the hook)
* _input_ Token (Secret token to validate received payloads)
* _output_ Hook ID 

![Create Project Webhook](images/create_project_webhook.png)

#### Create Tag
Properties:
* _input_ GitLab Server 
* _input_ API Key (Optionally, override the GitLab Server configuration API token)
* _input_ Project ID (This is visible in the GUI and should be an integer)
* _input_ Reference (Commit hash, another tag name, or branch name from which to create the tag)
* _input_ Tag Name 
* _input_ Message (An optional description for the tag)
* _output_ Commit ID (The hash of the commit for the tag)

![Create Tag](images/create_tag.png)

#### Query Commits
Properties:
* _input_ GitLab Server 
* _input_ API Key (Optionally, override the GitLab Server configuration API token)
* _input_ Project ID (This is visible in the GUI and should be an integer)
* _input_ Branch Name (If not provided, the default branch will be used)
* _input_ Results Limit (Upper limit on the number of commits to return from the query)
* _output_ Commits 

![Query Commits](images/query_commits.png)

#### Query Data
Properties:
* _input_ GitLab Server 
* _input_ API Key (Optionally, override the GitLab Server configuration API token)
* _input_ API Endpoint URI (URI for the API endpoint - for example /api/v4/projects/1/triggers.  Do not include URL parameters)
* _input_ JSON Path (The JSON path expression for locating the value of interest)
* _output_ Value 

![Query Data](images/query_data.png)

#### Query Merge Requests
Properties:
* _input_ GitLab Server 
* _input_ API Key (Optionally, override the GitLab Server configuration API token)
* _input_ Project ID (This is visible in the GUI and should be an integer)
* _input_ Results Limit (Upper limit on the number of pull requests to return from the query)
* _input_ Sorting (Approach for sorting query results)
* _input_ Simple View (If simple view is enabled, only the iid, URL, title, description, and basic state of the merge request are extracted)
* _input_ Source Branch (If a merge request source branch is provided, only matching merge requests will be returned.  For the value, provide a branch name, such as "master")
* _input_ Target Branch (If a merge request target branch is provided, only matching merge requests will be returned.  For the value, provide a branch name, such as "master")
* _input_ Milestone (Filter results by milestone.  For the value, provide a specific milestone, the value "Any", or the value "None")
* _input_ State 
* _output_ Merge Requests 

![Query Merge Requests](images/query_merge_requests.png)

#### Query Pipelines
Properties:
* _input_ GitLab Server 
* _input_ API Key (Optionally, override the GitLab Server configuration API token)
* _input_ Project ID (This is visible in the GUI and should be an integer)
* _output_ Pipelines 

![Query Pipelines](images/query_pipelines.png)

#### Query Project
Properties:
* _input_ GitLab Server 
* _input_ API Key (Optionally, override the GitLab Server configuration API token)
* _input_ Project Name 
* _input_ Namespace 
* _output_ Project ID 

![Query Project](images/query_project.png)

#### Query Secure Data
Properties:
* _input_ GitLab Server 
* _input_ API Key (Optionally, override the GitLab Server configuration API token)
* _input_ API Endpoint URI (URI for the API endpoint - for example /api/v4/projects/1/triggers.  Do not include URL parameters)
* _input_ JSON Path (The JSON path expression for locating the value of interest)
* _output_ Value 

![Query Data](images/query_secure_data.png)

#### Query Tags
Properties:
* _input_ GitLab Server 
* _input_ API Key (Optionally, override the GitLab Server configuration API token)
* _input_ Project ID (This is visible in the GUI and should be an integer)
* _Repository_ Search (Optionally, specify a search to filter what tags will be processed.  This uses the standard GitLab tags search criteria, so consult GitLab documentation on the syntax)
* _input_ Results Limit (Upper limit on the number of tags to return from the query)
* _output_ Tags 

![Query Tags](images/query_tags.png)

#### Trigger Pipeline
Properties:
* _input_ GitLab Server 
* _input_ API Key (Optionally, override the GitLab Server configuration API token)
* _input_ Project ID (This is visible in the GUI and should be an integer)
* _input_ Ref (Commit hash, tag name, or branch name from which to trigger the pipeline)
* _input_ Token (The token for the pipeline trigger.  This is not the same as the GitLab API access token)
* _input_ Variables (Optionally, provide variables to the pipeline execution)
* _output_ Pipeline ID 
* _output_ Pipeline Status 
* _output_ Pipeline Web URL 

![Trigger Pipeline](images/trigger_pipeline.png)

## Webhooks

### Code Commit/Push Webhook

#### Gitlab Webhook Configuration

Here's the URL Format :
```
http://username:password@xlrserver:port/api/extension/gitlab/commit_webhook?template=<templateName/prefix>
```

![Gitlab Webhook Configuration](images/commit_webhook_configure.png)

#### Release Summary view in XL Release
![Release Summary view in XL Release](images/commit_webhook_release.png)

#### Release Variables created
![Release Variables created](images/commit_webhook_variables.png)


### Merge Pull Request Webhook

#### Gitlab Webhook Configuration
```
http://username:password@xlrserver:port/api/extension/gitlab/pr_webhook?template=<templateName/prefix>
```

![Gitlab Webhook Configuration](images/pr_webhook_configure.png)

#### Release Summary view in XL Release
![Release Summary view in XL Release](images/pr_webhook_release.png)

#### Release Variables created
![Release Variables created](images/pr_webhook_variables.png)

### Triggers

#### Commit Trigger
Properties:
* _Repository_ GitLab Server 
* _Repository_ API Key (Optionally, provide an API token to override the server configuration)
* _Repository_ Project ID (GitLab project to monitor - should be an integer)
* _Repository_ Branch Name (Optionally, specify a branch name if only listening for commits on a single branch)
* _variables_ Commit Id (Commit hash)
* _variables_ Branch (Branch where the commit occurred)

#### Tag Trigger
Properties:
* _Repository_ GitLab Server 
* _Repository_ API Key (Optionally, provide an API token to override the server configuration)
* _Repository_ Project ID (GitLab project to monitor - should be an integer)
* _Repository_ Search (Optionally, specify a search to filter what tags will be processed.  This uses the standard GitLab tags search criteria, so consult GitLab documentation on the syntax)
* _variables_ Tag Name 
* _variables_ Tag Message 
* _variables_ Commit Id 
* _variables_ Commit Title 
* _variables_ Commit Message 
* _variables_ Commit Author 
* _variables_ Commit Committer 
* _variables_ Commit Creation Datetime 
* _variables_ Commit Authored Datetime 
* _variables_ Commit Committed Datetime 

### Tiles

Dashboard tiles are included in this plugin, to visualize commit, merge request, and pipelines information.  These tiles use the existing XL Release GitLab server configuration/connection and can be configured using the (usual dashboard setup approach)[https://docs.xebialabs.com/v.9.0/xl-release/get-started?subject=dashboards].  These dashboard titles are available for all dashboard scopes - release, folder, and global.

#### Commits Tile
Properties:
*  Title
* _input_ GitLab Server 
* _input_ API Key (Optionally, provide an API token to override the server configuration)
* _input_ Project ID (This is visible in the GUI and should be an integer)
* _input_ Branch Name (If not provided, the default branch will be used)
* _input_ Results Limit (Upper limit on the number of pull requests to return from the query)

#### Contributions Tile
Properties:
*  Title
* _input_ GitLab Server 
* _input_ API Key (Optionally, provide an API token to override the server configuration)
* _input_ Project ID (This is visible in the GUI and should be an integer)
* _input_ Branch Name (If not provided, the default branch will be used)
* _input_ Results Limit (Upper limit on the number of pull requests to return from the query)

#### Merge Requests Tile
Properties:
*  Title
* _input_ GitLab Server 
* _input_ API Key (Optionally, provide an API token to override the server configuration)
* _input_ Project ID (This is visible in the GUI and should be an integer)
* _input_ Results Limit (Upper limit on the number of pull requests to return from the query)
* _input_ Source Branch (If a merge request source branch is provided, only matching merge requests will be returned.  For the value, provide a branch name, such as "master")
* _input_ Target Branch (If a merge request target branch is provided, only matching merge requests will be returned.  For the value, provide a branch name, such as "master")

#### Pipelines Tile
Properties:
*  Title
* _input_ GitLab Server 
* _input_ API Key (Optionally, provide an API token to override the server configuration)
* _input_ Project ID (This is visible in the GUI and should be an integer)

#### Tags Timeline Tile
Properties:
*  Title
* _input_ GitLab Server 
* _input_ API Key (Optionally, provide an API token to override the server configuration)
* _input_ Project ID (This is visible in the GUI and should be an integer)
* _input_ Search (Optionally, specify a search to filter the tags.  This uses the standard GitLab tags search criteria, so consult GitLab documentation on the syntax)
* _input_ Results Limit (Upper limit on the count of latest tags to return from the query)

#### Timeline Tile
Properties:
*  Title
* _input_ GitLab Server 
* _input_ API Key (Optionally, provide an API token to override the server configuration)
* _input_ Project ID (This is visible in the GUI and should be an integer)
* _input_ Branch Name (If not provided, the default branch will be used)
* _input_ Results Limit (Upper limit on the number of pull requests to return from the query)


## Contributing

Please review the contributing guidelines for _xebialabs-community_ at [http://xebialabs-community.github.io/](http://xebialabs-community.github.io/)

## License

This community plugin is licensed under the [MIT license][https://opensource.org/licenses/MIT].

See license in [LICENSE.md](LICENSE.md)
