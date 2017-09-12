
from accTest.objectModel import baseTask
from accTest.objectModel import result


class Foo(baseTask.BaseTask):

    def __init__(self, *args, **kwargs):
        super(Foo, self).__init__(*args, **kwargs)
        self.executed = False

    def _run(self):
        self.executed = True
        return self.createResult(True)
