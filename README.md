[![Build Status](https://travis-ci.org/xebialabs-community/xlr-gitlab-plugin.svg?branch=master)](https://travis-ci.org/xebialabs-community/xlr-gitlab-plugin)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bf3bcce182d649eabb81183af545c80c)](https://www.codacy.com/app/erasmussen39/xlr-gitlab-plugin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xebialabs-community/xlr-gitlab-plugin&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/080f8c6a66e9d765d11e/maintainability)](https://codeclimate.com/github/xebialabs-community/xlr-gitlab-plugin/maintainability)
[![License: MIT][xlr-gitlab-plugin-license-image] ][xlr-gitlab-plugin-license-url]
[![Github All Releases][xlr-gitlab-plugin-downloads-image]]()

[xlr-gitlab-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-gitlab-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-gitlab-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-gitlab-plugin/total.svg

# Preface #

This document describes the functionality provided by the xlr-github-plugin.

See the **XL Release Reference Manual** for background information on XL Release and release concepts.

# Overview #

The xlr-github-plugin is a XL Release plugin that allows to
  * Create a merge request in GitLab
  * Accept a merge request in GitLab

## Types ##

+ Create Merge Request
  * 'project_id' : Numerical Project ID
  * 'source_branch' : Source branch for the merge request
  * 'target_branch' : Target branch for the merge request
  * 'title' : Title for the merge request
  * 'API Key' : Optional substitute API Key
  * 'Merge ID' : Merge ID returned from GitLab

+ Accept Merge Request
  * 'project_id' : Numerical Project ID
  * 'merge_id' : Merge ID to accept
  * 'API Key' : Optional substitute API Key

+ GitLab Server
  * 'address' : URL for GitLab
  * 'API Key' : API key to use
