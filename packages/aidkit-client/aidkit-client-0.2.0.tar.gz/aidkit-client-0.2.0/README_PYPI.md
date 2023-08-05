![aidkit](https://www.neurocat.ai/wp-content/uploads/2018/11/addkit-hori.png)

aidkit is an MLOps platform that allows you to assess and defend against threads
and vulnerabilities of AI models before they deploy to production.
aidkit-client is a companion python client library to seamlessly integrate with
aidkit in python projects.

## Changelog

Breaking changes are written in bold text.

### Version 0.2.0

* **Rename `resources.Report.table` to `resources.Report.table_string`.**
* Add `resources.Report.table` function returning a pandas dataframe.
* **Move `endpoints` module to `_endpoints`.**
* **Remove class `aidkit.Aidkit`.**
* Add docstrings.
* **Rename `exceptions.AidkitCLIError` to `exceptions.AidkitClientError`.**
* Add class `exceptions.AuthenticationError`, which is raised whenever the client fails to authenticate to the server.
* Include http error code and http body returned by the aidkit server in all exceptions.
* Make http request timeout configurable.
* Add `id` and `name` properties to resources.
* Add option to use progress bar in `PipelineRun.report` and `MLModelVersion.upload`.
* Add `PipelineRun.get_progress` method, which can be used to check how far a pipeline run has progressed.
* **Update web API version**.
* Add functionality to manage datasets and subsets from the client including data upload with added resources
`Dataset` and `Observation` and updated resource `Subset`.
* Add functionality to download artifacts from the report.
