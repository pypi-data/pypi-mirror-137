import os
import time

import pytest


def pytest_addoption(parser):
    group = parser.getgroup(
        'tryton', 'Tryton testing configuration')
    group.addoption(
        "--config",
        action="store",
        default="etc/test.cfg",
        help="Tryton configuration file. Defaults to etc/test.cfg",
    )
    group.addoption(
        "--db-cache",
        action="store",
        default=os.environ.get('DB_CACHE', 'db-cache'),
        help="Database cache folder. Environment DB_CACHE by default.",
    )


def pytest_sessionstart(session):

    os.environ['TRYTOND_CONFIG'] = session.config.getoption('--config')
    os.environ['DB_CACHE'] = session.config.getoption('--db-cache')

    from trytond.config import config

    config.update_etc()

    # Import after application is configured
    import trytond.backend

    # See https://bugs.tryton.org/issue8836
    if tuple(trytond.__version__.split('.')) < ('5', '6'):
        backend_name = trytond.backend.name()
    else:
        backend_name = trytond.backend.name

    if backend_name == 'sqlite':
        database_name = ':memory:'
    else:
        database_name = 'test_' + str(int(time.time()))

    os.environ.setdefault('DB_NAME', database_name)


@pytest.fixture(scope='session')
def trytond_modules():
    """Override to set what modules will be activated by
    the ``activate_modules`` fixture, ``['tests']`` by default."""
    yield ['tests']


@pytest.fixture(scope='session')
def activate_module(trytond_modules):
    """Override the ``trytond_modules`` fixture to set what modules
    will be activated, ``['tests']`` by default.
    """
    # FIXME: Make the activate_module fixture
    # execute only once with pytest-xdist
    #
    # https://pytest-xdist.readthedocs.io/en/latest/how-to.html#making-session-scoped-fixtures-execute-only-once

    from trytond.tests.test_tryton import ModuleTestCase

    class X(ModuleTestCase):
        module = trytond_modules[0]
        extras = trytond_modules[1:]

    X.setUpClass()
    yield
    X.tearDownClass()


@pytest.fixture
def transaction(activate_module):
    """Start and yield a transaction that will be rollbacked."""
    from trytond.cache import Cache
    from trytond.transaction import Transaction
    from trytond.tests.test_tryton import DB_NAME
    tt = Transaction()
    # FIXME reuse `trytond.tests.test_tryton:with_transaction`
    # instead of rewriting its implementation.
    with tt.start(DB_NAME, 1, context={}):
        try:
            yield tt
        finally:
            tt.rollback()
            Cache.drop(DB_NAME)
