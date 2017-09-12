
import os


class ResourceDir(object):

    path = ''


def findResourceDir(entryPath):
    dirPath = os.path.dirname(entryPath)
    while dirPath not in ('', os.path.sep):
        expectedResourceDir = os.path.join(dirPath, 'resources')
        if os.path.isdir(expectedResourceDir):
            return expectedResourceDir
        dirPath = os.path.dirname(dirPath)
    return ''


def filePath(fileName):
    if not ResourceDir.path:
        ResourceDir.path = findResourceDir(__file__)
    return os.path.join(ResourceDir.path, fileName)


def path():
    return filePath('')


def currentPak():
    for pakName in os.environ.get('PAK_PKG_LIST', '').split(os.path.pathsep):
        if pakName.startswith('accTest-'):
            return pakName
    return ''
