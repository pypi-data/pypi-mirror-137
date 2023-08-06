# -*- coding: utf-8 -*-

import pytest
import artefacts


def pytest_addoption(parser):
    group = parser.getgroup('dbt-conventions')
    group.addoption(
        '--foo',
        action='store',
        dest='dest_foo',
        default='2022',
        help='Set the value for the fixture "bar".'
    )


@pytest.fixture
def bar(request):
    return request.config.option.dest_foo


@pytest.fixture
def dbt_test_fixture():
    return 'dbt-conventions!!!'
