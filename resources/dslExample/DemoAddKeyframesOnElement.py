

from accTest.objectModel import baseTask


class DemoAddKeyframesOnElement(baseTask.BaseTask):

    def __init__(self, *args, **kwargs):
        super(DemoAddKeyframesOnElement, self).__init__(*args, **kwargs)
        self.executed = False

    def _run(self):
        self.executed = True
        return self.createResult(True)
