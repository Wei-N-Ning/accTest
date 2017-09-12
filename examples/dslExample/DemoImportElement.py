
from maya import cmds

import hydra
import athena

from accTest.objectModel import baseTask


class DemoImportElement(baseTask.BaseTask):

    def __init__(self, *args, **kwargs):
        super(DemoImportElement, self).__init__(*args, **kwargs)
        self.executed = False

    def _run(self):
        self.executed = True
        return self.createResult(True)
