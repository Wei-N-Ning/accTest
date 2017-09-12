
import os

from accTest.objectModel import baseTask

from moTest import finder


class DemoSharedTask(baseTask.BaseTask):

    def __init__(self, *args, **kwargs):
        super(DemoSharedTask, self).__init__(*args, **kwargs)
        self.executed = False

    def _run(self):
        self.executed = True
        return self.createResult(True)


class HydraProductExists(baseTask.BaseTask):
    """
    Require properties:

    hydraGroup
    productType
    productName
    """

    def __init__(self, *args, **kwargs):
        super(HydraProductExists, self).__init__(*args, **kwargs)

    def _errorMsg(self, group, productType, productName):
        return '{} does not have product: type({}), name({})'.format(group, productType, productName)

    def _run(self):
        import hydra
        f = self.getFixture()
        productType = f.getValue('productType')
        productName = f.getValue('productName')
        group = hydra.getGroup(f.getValue('hydraGroup'))
        if group.hasProduct(productType, productName):
            return self.success()
        else:
            f.terminate()
            return self.fatal(msg=self._errorMsg(group, productType, productName))


class HydraVersionExists(baseTask.BaseTask):

    def __init__(self, *args, **kwargs):
        super(HydraVersionExists, self).__init__(*args, **kwargs)

    def _errorMsg(self, group, productType, productName, version):
        return 'Product (type/name) {}/{} in group {} does not have a version {}'.format(
            productType, productName, group, version
        )

    def _run(self):
        import hydra
        f = self.getFixture()
        productType = f.getValue('productType')
        productName = f.getValue('productName')
        version = f.getValue('version')
        group = hydra.getGroup(f.getValue('hydraGroup'))
        try:
            product = group.getProduct(productType, productName)
            product.getVersion(version)
        except hydra.HydraException, e:
            f.terminate()
            return self.fatal(self._errorMsg(group, productType, productName, version))
        return self.success()


class RunRepositoryTests(baseTask.BaseTask):

    def _run(self):
        fixture = self.getFixture()
        dirPath = fixture.getValue('dirPath')
        pattern = fixture.getValue('pattern')

        if not (dirPath and os.path.isdir(dirPath)):
            fixture.terminate()
            return self.fatal('Tests tree does not exist: {}'.format(dirPath))
        retCode = finder.runTestsInDir(dirPath, pattern=pattern)
        if not retCode:
            fixture.terminate()
            return self.fatal('One or more tests have failed: {}'.format(dirPath))
        return self.success(dirPath)


class SelectElement(baseTask.BaseTask):

    def _run(self):
        import redbox
        fixture = self.getFixture()
        rbws = fixture.getValue('rbws')
        elementName = fixture.getValue('elementName')
        rbElem = rbws.getElementsByName(elementName)[0]
        redbox.cmds.select(rbElem)
        return self.success('selected: {}'.format(elementName))


class RunActionOnElement(baseTask.BaseTask):

    def _run(self):
        fixture = self.getFixture()
        actionName = fixture.getValue('actionName') or ''
        rbws = fixture.getValue('rbws')
        elementName = fixture.getValue('elementName')
        rbElem = rbws.getElementsByName(elementName)[0]
        rbElem.executeAction(actionName)
        return self.success('action: {}, element: {}'.format(actionName, elementName))


class LoadRedboxWorkspace(baseTask.BaseTask):

    def _run(self):
        import redbox
        fixture = self.getFixture()
        workspaceFilePath = fixture.getValue('workspaceFilePath')
        if not (workspaceFilePath and os.path.isfile(workspaceFilePath)):
            return self.fatal('workspace file does not exist: {}'.format(workspaceFilePath))
        rbws = redbox.Workspace(path=workspaceFilePath)
        if fixture.getValue('isShared'):
            rbws.setShared()
        if fixture.getValue('doLoad'):
            rbws.load()
        fixture.setValue('rbws', rbws)
        return self.success(str(rbws))


class MotionbuilderFileNew(baseTask.BaseTask):

    def _run(self):
        import pyfbsdk
        app = pyfbsdk.FBApplication()
        return self.success(str(app.FileNew()))


class MotionbuilderFindModel(baseTask.BaseTask):

    def _findModel(self, modelName):
        import pyfbsdk
        api = pyfbsdk.FBSystem()
        sceneRoot = api.Scene.RootModel
        for model in sceneRoot.Children:
            if model.Name == modelName:
                return model
        return None

    def _run(self):
        fixture = self.getFixture()
        modelName = fixture.getValue('modelName')
        model = self._findModel(modelName)
        if model is not None:
            fixture.setValue('model', model)
            return self.success(str(model))
        fixture.terminate()
        return self.fatal('Can not find model: {}'.format(modelName))

