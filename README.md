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

