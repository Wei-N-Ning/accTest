
import os

from accTest.objectModel import baseTask


class AssertCharMapPublish(baseTask.BaseTask):

    def _run(self):
        fixture = self.getFixture()
        hydraVersion = fixture.getValue('hydraVersion')
        hydraResource = hydraVersion.getResources()[0]
        filePath = hydraResource.location
        if filePath and os.path.isfile(filePath):
            return self.success(filePath)
        return self.fatal('Resource file does not exist.')
