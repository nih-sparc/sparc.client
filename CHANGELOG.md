# CHANGELOG

## [v0.3.0] - 2024-03-12
### :bug: Bug Fixes
- [`e4457a1`](https://github.com/nih-sparc/sparc.client/commit/e4457a1e783fdd4bdaad259de5b4e64f271ed20c) - no additional permissions needed, would need to run on vulnerable: pull_request_target *(commit by [@athril](https://github.com/athril))*
- [`a8b1754`](https://github.com/nih-sparc/sparc.client/commit/a8b17546d4988a2036df66451abb94c85b217740) - code reformatting *(commit by [@athril](https://github.com/athril))*
- [`0a419f6`](https://github.com/nih-sparc/sparc.client/commit/0a419f6f95b37669c5c8f44fb126c3e6aaae6351) - reformatting back *(commit by [@athril](https://github.com/athril))*

### :wrench: Chores
- [`2cb1b77`](https://github.com/nih-sparc/sparc.client/commit/2cb1b77e3faca44089f483ad323656b5aa01f985) - expanding CI by adding coverage report *(commit by [@athril](https://github.com/athril))*
- [`ff59969`](https://github.com/nih-sparc/sparc.client/commit/ff59969313c37a548282e64a0f9e476d77b444a5) - adding protection for sphinx workflow *(commit by [@athril](https://github.com/athril))*
- [`08683bb`](https://github.com/nih-sparc/sparc.client/commit/08683bb2a0f00f11f0898978e96236ce26f7c479) - an automated pipeline to release new version on Github and PyPI *(commit by [@athril](https://github.com/athril))*
- [`ee07918`](https://github.com/nih-sparc/sparc.client/commit/ee0791851daea7d0ea0dd48a3db5bfee96fbefaa) - dynamic versioning of PyPI package with setuptools_scm *(commit by [@athril](https://github.com/athril))*
- [`37431b4`](https://github.com/nih-sparc/sparc.client/commit/37431b42ead4eae38d8adbacafabb78bbb82f292) - fixing PyPI deployment *(commit by [@athril](https://github.com/athril))*
- [`b485c9e`](https://github.com/nih-sparc/sparc.client/commit/b485c9e6c3d827a9abe1f0f1ab95e981e5ff31aa) - removing commented lines *(commit by [@athril](https://github.com/athril))*
- [`65e0c75`](https://github.com/nih-sparc/sparc.client/commit/65e0c7528803a3d1292526830574213c1f2b55bd) - limiting scope of Sphinx workflow launch *(commit by [@athril](https://github.com/athril))*
- [`676b1f9`](https://github.com/nih-sparc/sparc.client/commit/676b1f9f7d34a661c03fd62b0d11fde48a16e938) - adding CODECOV token to prepare for codecov-action@v4 (currently in beta) *(commit by [@athril](https://github.com/athril))*
- [`7341eae`](https://github.com/nih-sparc/sparc.client/commit/7341eaebf1323a1aa98150038b321d6da190f42b) - fixing reviewdog permissions *(commit by [@athril](https://github.com/athril))*
- [`4119d2e`](https://github.com/nih-sparc/sparc.client/commit/4119d2ebf0bad418895f505704d3b36da5fb376c) - fixing reviewdog permissions *(commit by [@athril](https://github.com/athril))*
- [`2afa0eb`](https://github.com/nih-sparc/sparc.client/commit/2afa0eb4ca6260ce1438d6bceb796c7b90a2d6c2) - fixing reviewdog permissions *(commit by [@athril](https://github.com/athril))*
- [`ea66084`](https://github.com/nih-sparc/sparc.client/commit/ea660848a269fb9b842c2db2e42a0d586ab23886) - reviewdog permissions *(commit by [@athril](https://github.com/athril))*
- [`b70d867`](https://github.com/nih-sparc/sparc.client/commit/b70d8672d202e25a7b74058a290063c3eb6eef9b) - reviewdog permissions *(commit by [@athril](https://github.com/athril))*
- [`38cc7c4`](https://github.com/nih-sparc/sparc.client/commit/38cc7c4b730b52e8176f3be17146acb10163d9bc) - fixing outdated versions of actions *(commit by [@athril](https://github.com/athril))*


## [v0.2.0]

### :sparkles: New features

- Added O2SparcService service:

  * Introduced a `O2SparcSolver` class which is the main class for running computational jobs on o²S²PARC. This class holds the following methods:
  * `submit_job`
  * `get_job_progress`
  * `job_done`
  * `get_results`
  * `get_job_log`

- Introduced `get_solver` method to `O2SparcService` which returns a `O2SparcSolver` object

- Scaffold Retrieval:

  * Introducing the ability to use `sparc.client` to retrieve scaffolds or scaffold descriptions.
  * The retrieved scaffold or scaffold description files can now be converted to a commonly used mesh format, such as VTK.
  * Reuse of packages from the mapping tools codebase ensures efficient and standardized mesh conversion.

- MBF Segmentation Export:

  * Added support for exporting MBF Segmentation data to a commonly used mesh format, like VTK.

- Segmentation Data Analysis:

  * New functionality to analyze a given segmentation data file for suitability in the mapping tools fitting workflow, and provide a clear and informative report.

- Updated Documentation:

  * Added the [SPARC Python Zinc Client tutorial](https://github.com/nih-sparc/sparc.client/blob/main/docs/tutorial-zinc.ipynb) to reflect the features related to Zinc.


## [v0.1.0]

### :bug: Bug Fixes

- download multiple files from Pennsieve #12
- pennsieve Download file API #14
- Github action updates: Reviewdog should run whenever a PR is modified after opening #15
- new tutorial in Jupyter Notebook
- README.md update

## [v0.0.2]

Alpha2 release of Python Sparc Client.

### :sparkles: New features

- Code coverage at 100%
- Sphinx documentation with Github Pages

## [v0.0.1]

Alpha release of Python Sparc Client.

### :sparkles: New features

- automatic/manual module loading
- ServiceBase class for adding new modules
- Pennsieve module with basic functionalities:
  * listing datasets, files, records
  * downloading files
  * Basic API support (GET/POST)

[v0.3.0]: https://github.com/nih-sparc/sparc.client/compare/v0.2.0...v0.3.0