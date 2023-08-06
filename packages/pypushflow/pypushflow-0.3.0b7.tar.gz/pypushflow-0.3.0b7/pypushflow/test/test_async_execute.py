import sys
import unittest
import itertools
from threading import Event
from contextlib import contextmanager
from pypushflow.AsyncExecute import ProcessPool
from pypushflow.AsyncExecute import apply_async


def add(a, b):
    return a + b


def error(a, b):
    raise RuntimeError("intentional error")


class TestAsyncExecute(unittest.TestCase):
    def setUp(self) -> None:
        self.callback_event = Event()
        self.failed_msg = ""

    def reset(self):
        self.callback_event.clear()
        self.failed_msg = ""

    @property
    def contexts(self):
        if sys.platform != "win32":
            return [None, "fork", "spawn", "forkserver"]
        else:
            return [None, "spawn"]

    def test_async_execution(self):
        context = self.contexts
        daemon = [True, False]
        manage_pool = [True, False]
        processes = [None, 1]
        functions = [add, error]
        for context, daemon, manage_pool, processes, func in itertools.product(
            context, daemon, manage_pool, processes, functions
        ):
            pool_options = {
                "context": context,
                "daemon": daemon,
                "manage_pool": manage_pool,
                "processes": processes,
            }
            with self.subTest(func=func.__name__, **pool_options):
                self.run_test(func, **pool_options)

    @contextmanager
    def run_context(self, manage_pool=True, **pool_options):
        self.reset()
        if manage_pool:
            pool = None
            try:
                with ProcessPool(**pool_options) as pool:
                    yield {"pool": pool}
            finally:
                if pool is not None:
                    pool.join()
        else:
            yield pool_options

    def run_test(self, func, **pool_options):
        with self.run_context(**pool_options) as pool_options:
            apply_async(
                func,
                args=(1, 1),
                callback=self._result_callback,
                error_callback=self._error_callback,
                **pool_options,
            )
            self.callback_event.wait(5)
            self.assertFalse(bool(self.failed_msg), msg=self.failed_msg)

    def _result_callback(self, return_value):
        try:
            if return_value != 2:
                self.failed_msg = f"{return_value} != 2"
        finally:
            self.callback_event.set()

    def _error_callback(self, exception):
        try:
            if not isinstance(exception, RuntimeError):
                self.failed_msg = f"{exception} is not a RuntimeError"
            elif str(exception) != "intentional error":
                self.failed_msg = f"'{exception}' != 'intentional error'"
        finally:
            self.callback_event.set()
