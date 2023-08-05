import multiprocessing
import multiprocessing.pool

NONDAEMONIC_CONTEXTS = dict()

for base_context in [None, "fork", "spawn", "spawnserver"]:
    try:
        BaseContext = type(multiprocessing.get_context(base_context))
    except Exception:
        continue

    class NoDaemonProcess(BaseContext.Process):
        """
        Non-daemonic processes
        See : https://stackoverflow.com/a/53180921
        """

        @property
        def daemon(self):
            return False

        @daemon.setter
        def daemon(self, value):
            pass

    class NoDaemonContext(BaseContext):
        Process = NoDaemonProcess

    NONDAEMONIC_CONTEXTS[base_context] = NoDaemonContext()


class ProcessPool(multiprocessing.pool.Pool):
    """Pool that can also manage non-daemonic processes.

    Processes from multiprocessing are daemonic by default which means:
    * the subprocess is automatically terminated after the parent process
      ends to prevent orphan processes
    * the subprocess cannot start another subprocess

    By default it uses daemonic processes which cannot have subprocesses
    and "fork" context (on Linux) or "spawn" context (on Win32).
    """

    # We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
    # because the latter is only a wrapper function, not a proper class.

    def __init__(self, **kwargs):
        context = kwargs.pop("context", None)
        daemon = kwargs.pop("daemon", True)
        if not daemon:
            kwargs["context"] = NONDAEMONIC_CONTEXTS.get(context)
        super().__init__(**kwargs)

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
    daemon=True,
    context=None,
):
    """Launch a function in a subprocess with callbacks.

    By default it uses a daemonic process which cannot have subprocesses
    and "fork" context (on Linux) or "spawn" context (on Win32).
    """
    pool = ProcessPool(processes=1, daemon=daemon, context=context)

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
