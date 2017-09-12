
import hydra
import athena

from accTest.objectModel import baseTask


class DemoAssertKeyframesOnElement(baseTask.BaseTask):

    def __init__(self, *args, **kwargs):
        super(DemoAssertKeyframesOnElement, self).__init__(*args, **kwargs)
        self.executed = False

    def _run(self):
        self.executed = True
        return self.createResult(True)
