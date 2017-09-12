
import tempfile

from accTest.objectModel import baseTask


class GenerateCharMap(baseTask.BaseTask):

    def _run(self):
        filePath = self.createCharMapFile()
        fixture = self.getFixture()
        fixture.setValue('filePath', filePath)
        return self.success(filePath)

    @staticmethod
    def createCharMapFile(pathAllocator=None, generator=None):
        """

        Args:
            pathAllocator (callable): a function-like object that allocates a file path
            generator (callable): a function-like object that takes a file pointer and writes out the char-map content
        """

        if pathAllocator:
            filePath = pathAllocator()
        else:
            notUsed_, filePath = tempfile.mkstemp(prefix='AccTest_GenerateCharMap', suffix='.cm')
        with open(filePath, 'w') as fp:
            if generator:
                generator(fp)
            else:
                fp.write("{version: 1.0}\n")
        return filePath


class GenerateCharMap__step_1(baseTask.BaseTask):

    def _run(self):
        return self.fatal('Not implemented')


class GenerateCharMap__step_2(baseTask.BaseTask):

    def _run(self):
        return self.fatal('Not implemented')

    @staticmethod
    def createTemporaryCharMapFile():
        notUsed_, filePath = tempfile.mkstemp(prefix='AccTest_GenerateCharMap', suffix='.cm')
        with open(filePath, 'w') as fp:
            fp.write('Bio Character Map File\nv1.00\n')
        return filePath


class GenerateCharMap__step_3(baseTask.BaseTask):

    def _run(self):
        filePath = self.createCharMapFile()
        fixture = self.getFixture()
        fixture.setValue('filePath', filePath)
        return self.success(filePath)

    @staticmethod
    def createCharMapFile(pathAllocator=None, generator=None):
        """

        Args:
            pathAllocator (callable): a function-like object that allocates a file path
            generator (callable): a function-like object that takes a file pointer and writes out the char-map content
        """

        if pathAllocator:
            filePath = pathAllocator()
        else:
            notUsed_, filePath = tempfile.mkstemp(prefix='AccTest_GenerateCharMap', suffix='.cm')
        with open(filePath, 'w') as fp:
            if generator:
                generator(fp)
            else:
                fp.write('Bio Character Map File\nv1.00\n')
        return filePath
