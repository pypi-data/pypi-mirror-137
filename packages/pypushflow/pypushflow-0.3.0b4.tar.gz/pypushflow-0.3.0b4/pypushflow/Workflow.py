#
# Copyright (c) European Synchrotron Radiation Facility (ESRF)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__authors__ = ["O. Svensson"]
__license__ = "MIT"
__date__ = "28/05/2019"


import pprint
import logging
from contextlib import contextmanager
from pypushflow.persistence import db_client
from pypushflow.logutils import PyPushflowLoggedObject
from pypushflow.logutils import basicConfig
from pypushflow.AsyncExecute import ProcessPool


class Workflow(PyPushflowLoggedObject):
    def __init__(self, name, daemon=False, context=None, level=logging.DEBUG):
        basicConfig(filename=name, level=level)
        super().__init__(log_metadata={"workflow": name})
        self.logger.info("\n\nStarting new workflow '%s'\n", name)
        self.name = name
        self.listOnErrorActor = []
        self.db_client = db_client()
        self.db_client.startWorkflow(name)
        self.listActorRef = []
        self.pool_options = {"daemon": daemon, "context": context}
        self.__pool = None

    def connectOnError(self, actor):
        self.logger.debug("connect to error handler '%s'", actor.name)
        self.listOnErrorActor.append(actor)

    def triggerOnError(self, inData):
        self.logger.info(
            "triggered due to error with inData =\n %s", pprint.pformat(inData)
        )
        for onErrorActor in self.listOnErrorActor:
            onErrorActor.trigger(inData)

    def getActorPath(self):
        return "/" + self.name

    def addActorRef(self, actorRef):
        self.logger.debug("add reference to actor '%s'", actorRef.name)
        self.listActorRef.append(actorRef)

    def getListActorRef(self):
        return self.listActorRef

    def setStatus(self, status):
        self.db_client.setWorkflowStatus(status)

    @property
    def pool(self):
        return self.__pool

    @contextmanager
    def _run_context(self, shared_pool=False):
        if not shared_pool:
            # A new pool with 1 worker will be created for each asynchronous
            # call and the pool cleanup is done in the callbacks
            yield
            return
        if self.__pool is not None:
            # A pool already exists
            yield
            return
        processes = sum(actor.pool_resources for actor in self.listActorRef)
        try:
            with ProcessPool(processes=processes, **self.pool_options) as pool:
                self.__pool = pool
                yield
        finally:
            if self.__pool is not None:
                self.__pool.join()
                self.__pool = None

    def run(self, inData, timeout=None, shared_pool=False):
        with self._run_context(shared_pool=shared_pool):
            self.startActor.trigger(inData)
            self.stopActor.join(timeout=timeout)
            return self.stopActor.outData
