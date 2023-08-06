import os

import pytest

from artefacts.config import conf
from artefacts.core import Manifest, RunResults, Sources, Catalog
import artefacts.api


# TODO: enable configuration via pytest args.
# Currently the import of artefacts.config initializes the conf.
# But I think we can override the values on the config if necessary.
# def pytest_addoption(parser):
#     group = parser.getgroup('dbt-conventions')
#     group.addoption(
#         '--dbt-project-dir',
#         action='store',
#         dest='dest_dbt_project_dir',
#         default=os.getcwd(),
#         help='Path to the dbt project directory, defaults to the current working directory.'
#     )


@pytest.fixture(scope='session')
def artefacts_conf(request):
    return conf


@pytest.fixture(scope='session')
def manifest(artefacts_conf):
    return Manifest.load()


@pytest.fixture(scope='session')
def run_results(artefacts_conf):
    return RunResults.load()


@pytest.fixture(scope='session')
def catalog(artefacts_conf):
    return Catalog.load()


@pytest.fixture(scope='session')
def sources(artefacts_conf):
    return Sources.load()    


@pytest.fixture(scope='session', params=artefacts.api.models(), ids=[m.unique_id for m in artefacts.api.models()])
def model(request):
    yield request.param


@pytest.fixture(scope='session', params=artefacts.api.tests(), ids=[n.unique_id for n in artefacts.api.tests()])
def test(request):
    yield request.param


@pytest.fixture(scope='session', params=artefacts.api.seeds(), ids=[n.unique_id for n in artefacts.api.seeds()])
def seed(request):
    yield request.param


@pytest.fixture(scope='session', params=artefacts.api.sources(), ids=[n.unique_id for n in artefacts.api.sources()])
def source(request):
    yield request.param


@pytest.fixture(scope='session', params=artefacts.api.exposures(), ids=[n.unique_id for n in artefacts.api.exposures()])
def exposure(request):
    yield request.param


@pytest.fixture(scope='session', params=artefacts.api.metrics(), ids=[n.unique_id for n in artefacts.api.metrics()])
def metric(request):
    yield request.param


@pytest.fixture(scope='session', params=artefacts.api.macros(), ids=[n.unique_id for n in artefacts.api.macros()])
def macro(request):
    yield request.param


@pytest.fixture(scope='session', params=[v for v in artefacts.api.selectors()], ids=[k for k,v in artefacts.api.selectors()])
def selector(request):
    yield request.param

