# pypushflow

A task scheduler for cyclic and acyclic graphs

## Install

```bash
python -m pip install pypushflow[mx]
```

Use the `mx` option for installation at MX beamlines.

## Run tests

```bash
python -m pip install pypushflow[test]
pytest
```


## Getting started

```python
import logging
from pypushflow.Workflow import Workflow
from pypushflow.StopActor import StopActor
from pypushflow.StartActor import StartActor
from pypushflow.PythonActor import PythonActor
from pypushflow.ThreadCounter import ThreadCounter


class MyWorkflow(Workflow):
    """
    Workflow containing one start actor,
    one python actor and one stop actor.
    """

    def __init__(self, name):
        super().__init__(name, level=logging.DEBUG)
        ctr = ThreadCounter(parent=self)
        self.startActor = StartActor(parent=self, thread_counter=ctr)
        self.pythonActor = PythonActor(
            parent=self,
            script="pypushflow.test.pythonActorTest.py",
            name="Python Actor Test",
            thread_counter=ctr,
        )
        self.stopActor = StopActor(parent=self, thread_counter=ctr)
        self.startActor.connect(self.pythonActor)
        self.pythonActor.connect(self.stopActor)


testMyWorkflow = MyWorkflow("Test workflow 1")
inData = {"name": "Jerry"}
outData = testMyWorkflow.run(inData, timeout=15, shared_pool=True)
assert outData["reply"] == "Hello Jerry!"
```