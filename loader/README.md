# Intro

https://github.com/climatepolicyradar/navigator/issues/49

The first step is to get the original transformation + loading code from
the [Jupyter notebook](https://github.com/climatepolicyradar/cpr/blob/master/nbs/policy-etl.ipynb) and
the [CLI](https://github.com/climatepolicyradar/policy-search/blob/dev/cli.py) into the codebase alongside the backend.
A first version of the loader will do all the steps (transformation and loading) in one process, and the steps can be
decoupled later.

The transformer can ingest data from known local CCLW CSVs, and then later,
a [separate document ingest service](https://docs.google.com/drawings/d/1kZqhN3V4O_B1djmwQmtibyOxwqInoLycUUGToiJvD_8/edit)
can provide inputs to the loader.
