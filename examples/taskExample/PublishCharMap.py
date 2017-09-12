
import shutil

from accTest.objectModel import baseTask

import athena


class PublishCharMap(baseTask.BaseTask):

    def _run(self):
        fixture = self.getFixture()
        hydraGroup = fixture.getValue('hydraGroup')
        productType = fixture.getValue('productType')
        productName = fixture.getValue('productName')
        ph = self.createProductHandler(hydraGroup, productType, productName)
        filePath = fixture.getValue('filePath')
        hydraVersion = self.publishCharMapFile(ph, filePath)
        fixture.setValue('hydraVersion', hydraVersion)
        return self.success(str(ph.getVersion()))

    @staticmethod
    def createProductHandler(hydraGroup, productType, productName):
        context = athena.environment.getAccessorContextFromOzArea(hydraGroup)
        context['element'] = productName
        context['usageType'] = 'demo'
        context['fileType'] = 'txt'
        return athena.ProductHandler(productType, context)

    @staticmethod
    def publishCharMapFile(productHandler, filePath):
        acc = productHandler.getAccessor()
        acc.createProduct()
        ver = acc.reserveVersion()
        pathToWrite = acc.buildPath('cm')
        shutil.copy(filePath, pathToWrite)
        ver.createResource('cm', location=pathToWrite)
        acc.finalizeVersion()
        acc.publishVersion(attributes={'source': __file__})
        return ver


class PublishCharMap__step_1(baseTask.BaseTask):

    def _run(self):
        return self.fatal('Not implemented!')


class PublishCharMap__step_2(baseTask.BaseTask):

    def _run(self):
        fixture = self.getFixture()
        hydraGroup = fixture.getValue('hydraGroup')
        productType = fixture.getValue('productType')
        productName = fixture.getValue('productName')
        ph = athena.ProductHandler()
        filePath = fixture.getValue('filePath')
        return self.fatal('Not implemented!')
