
import hydra
import athena

from maya import cmds

from accTest.objectModel import baseTask


class DemoExportElement(baseTask.BaseTask):

    def __init__(self, *args, **kwargs):
        super(DemoExportElement, self).__init__(*args, **kwargs)
        self.executed = False

    def _run(self):
        self.executed = True
        return self.createResult(True)
