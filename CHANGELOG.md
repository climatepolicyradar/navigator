# Releases

## Future

* Squash migrations to remove data migrations (to be done with separate SQL scripts)
    Process to deploy should be to remove the single row in `alembic_version`.
    After the migrations are run this should become `0001`

## v0.9.6-alpha

* Enable self-registration
* Structured Logging
* Moved pdf-parser to separate repo: [navigator-pdf-parser](https://github.com/climatepolicyradar/navigator-pdf-parser)
* Moved search indexer to separate repo: [navigator-search-indexer](https://github.com/climatepolicyradar/navigator-search-indexer)
* Removed `common` subdirectory
* UI updates based on early-alpha feedback
* Various bugfixes resulting from early-alpha use
* Various deployment updates

## v0.9.5-alpha

* Fixed an issue in the password handling form that led to some passwords not being correctly recognised.

## v0.9.4-alpha

* Fix search caching bug when transitioning from landing page

## v0.9.3-alpha

* Pagination no longer displayed when no results returned
* Annotation highlighting on PDFs disabled
* UI Performance improvements
* Account management improvements

## v0.9.2-alpha

Fixed:
* Password resets no longer fail with "Token already redeemed"

## v0.9.1-alpha

* Merge pull request #645 from climatepolicyradar/release/0.9.1-alpha
* Switch dev/prod environments

## v0.9-alpha

* First alpha release
