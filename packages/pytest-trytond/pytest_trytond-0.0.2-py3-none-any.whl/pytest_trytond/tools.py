
import collections
import contextlib
import unittest.mock

import pytest

from trytond.pool import Pool
from trytond.transaction import Transaction
import trytond.tests.test_tryton


@pytest.mark.usefixtures('activate_module')
class ModuleTestCase(
    trytond.tests.test_tryton.ModuleTestCase
):
    "Module test case with no class setup/teardown"

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


@contextlib.contextmanager
def lazy_queue(run_at_exit=True):
    """Use as a context manager to locally patch Trytond's built-in
    queue system by actually calling all queued tasks at the exit of
    the context manager, simulating the behaviour of the RPC layer,
    or when later running the yielt object, simulating the behaviour
    of an active asynchronous worker service.
    """

    Queue = Pool().get('ir.queue')

    class queue:
        tasks = collections.deque()

        @classmethod
        def run(cls):
            for task_id in cls.tasks:
                # because queued tasks could queue more tasks!
                with lazy_queue():
                    Queue(task_id).run()

    with unittest.mock.patch(
            'trytond.transaction.Transaction.tasks',
            new_callable=unittest.mock.PropertyMock,
            return_value=queue.tasks
    ):
        yield queue

    if run_at_exit:
        queue.run()


@contextlib.contextmanager
def no_check_access():
    "Tweak transaction context to skip Tryton's record access rules"

    with Transaction().set_context(_check_access=False):
        yield


@contextlib.contextmanager
def supress_user_warnings():
    "Tweak transaction context to supress any user warning check"

    with Transaction().set_context(_skip_warnings=True):
        yield


@contextlib.contextmanager
def active_records(records):
    "Set active_id(s) and active_model in transaction's context"

    _record0 = records[0]
    with Transaction().set_context(
            active_id=_record0.id,
            active_ids=[rec.id for rec in records],
            active_model=_record0.__class__.__name__,
    ):
        yield
