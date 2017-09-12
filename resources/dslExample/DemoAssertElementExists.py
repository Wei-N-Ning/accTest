

from accTest.objectModel import baseTask


class DemoAssertElementExists(baseTask.BaseTask):

    def __init__(self, *args, **kwargs):
        super(DemoAssertElementExists, self).__init__(*args, **kwargs)
        self.executed = False

    def _run(self):
        self.executed = True
        return self.createResult(True)
