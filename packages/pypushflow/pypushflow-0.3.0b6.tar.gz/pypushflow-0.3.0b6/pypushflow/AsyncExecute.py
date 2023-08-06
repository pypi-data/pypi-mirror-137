"""Processes from python's multiprocessing package are daemonic by
default which means:

    * the subprocess is automatically terminated after the parent process
      ends to prevent orphan processes
    * the subprocess cannot start another subprocess

This module provides a process pool that can create daemonic and
non-daemonic processes.

See : https://stackoverflow.com/a/53180921
"""

import os
import sys
import multiprocessing
import multiprocessing.context
import multiprocessing.pool


class SpawnNonDaemonicProcess(multiprocessing.context.SpawnProcess):
    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, value):
        pass


class SpawnNonDaemonicContext(multiprocessing.context.SpawnContext):
    Process = SpawnNonDaemonicProcess


if sys.platform != "win32":

    class ForkNonDaemonicProcess(multiprocessing.context.ForkProcess):
        @property
        def daemon(self):
            return False

        @daemon.setter
        def daemon(self, value):
            pass

    class ForkServerNonDaemonicProcess(multiprocessing.context.ForkServerProcess):
        @property
        def daemon(self):
            return False

        @daemon.setter
        def daemon(self, value):
            pass

    class ForkNonDaemonicContext(multiprocessing.context.ForkContext):
        Process = ForkNonDaemonicProcess

    class ForkServerNonDaemonicContext(multiprocessing.context.ForkServerContext):
        Process = ForkServerNonDaemonicProcess

    if sys.platform == "darwin":
        NONDAEMONIC_CONTEXTS = {
            None: SpawnNonDaemonicContext,
            "spawn": SpawnNonDaemonicContext,
            "fork": ForkNonDaemonicContext,
            "forkserver": ForkServerNonDaemonicContext,
        }
    else:
        NONDAEMONIC_CONTEXTS = {
            None: ForkNonDaemonicContext,
            "spawn": SpawnNonDaemonicContext,
            "fork": ForkNonDaemonicContext,
            "forkserver": ForkServerNonDaemonicContext,
        }

else:
    NONDAEMONIC_CONTEXTS = {
        None: SpawnNonDaemonicContext,
        "spawn": SpawnNonDaemonicContext,
    }


class ProcessPool(multiprocessing.pool.Pool):
    """Process pool that can also manage non-daemonic processes.

    By default it uses daemonic processes (cannot have subprocesses)
    and "fork" context (on Linux) or "spawn" context (on Win32).
    """

    # We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
    # because the latter is only a wrapper function, not a proper class.

    def __init__(self, daemon=True, context=None, processes=None, **kwargs):
        if daemon:
            context = multiprocessing.get_context(context)
        elif context in NONDAEMONIC_CONTEXTS:
            context_class = NONDAEMONIC_CONTEXTS.get(context)
            context = context_class()
        if processes == "auto":
            processes = os.cpu_count() or 1
        super().__init__(context=context, processes=processes, **kwargs)

    def join(self):
        """Wait for all workers (subprocesses) to terminate.
        Call this after `terminate` or the process might not exit.
        """
        try:
            super().join()
        except RuntimeError as e:
            if str(e) != "cannot join current thread":
                raise

    def terminate(self, wait=False):
        super().terminate()
        if wait:
            self.join()


def apply_async(
    func,
    args=tuple(),
    kwds=None,
    callback=None,
    error_callback=None,
    pool=None,
    **pool_options
):
    """Execute a function in a subprocess with callbacks for the result."""
    if kwds is None:
        kwds = dict()

    if pool:
        return pool.apply_async(
            func, args=args, kwds=kwds, callback=callback, error_callback=error_callback
        )

    pool = ProcessPool(**pool_options)

    if callback is None:

        def _callback(return_value):
            pool.terminate(wait=True)

    else:

        def _callback(return_value):
            try:
                return callback(return_value)
            finally:
                pool.terminate(wait=True)

    if callback is None:

        def _error_callback(exception):
            pool.terminate(wait=True)

    else:

        def _error_callback(exception):
            try:
                return error_callback(exception)
            finally:
                pool.terminate(wait=True)

    future = pool.apply_async(
        func, args=args, kwds=kwds, callback=_callback, error_callback=_error_callback
    )
    pool.close()
    return future
