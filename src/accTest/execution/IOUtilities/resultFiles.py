
import glob
import os


class ResultFilesManager(object):

    def __init__(self, fileTemplate):
        self._outFileTemplate = fileTemplate
        self._outFilePaths = list()
        self._outFileIndex = 0

    def resetOutFiles(self):
        for filePath in self._outFilePaths:
            if os.path.isfile(filePath):
                os.remove(filePath)
        for filePath in glob.glob(self._outFileTemplate.format('*')):
            if os.path.isfile(filePath):
                os.remove(filePath)
        self._outFilePaths = list()

    def paths(self):
        return self._outFilePaths

    def outFilePath(self, create=False):
        if create:
            filePath = self._outFileTemplate.format(self._outFileIndex)
            self._outFilePaths.append(filePath)
            self._outFileIndex += 1
        else:
            if self._outFilePaths:
                filePath = self._outFilePaths[-1]
            else:
                raise ValueError('Can not find allocated result file.')
        return filePath
