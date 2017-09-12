
import os
import subprocess

from accTest import resources

import logging
logger = logging.getLogger(__name__)


class OzCmdLine(object):

    def __init__(self, ozExe=None, ozArea='/', using='', paksToAdd=None):
        self.ozArea = ozArea
        self.ozExe = ozExe if (ozExe and os.path.isfile(ozExe)) else \
            '/digi/var/oz/current/bin/bash_oz'
        self.using = using
        self.paksToAdd = list(paksToAdd) if paksToAdd else []
        self.paksToAdd.sort()

    @classmethod
    def createFromEnviron(cls, ozExe=None, environ=None):
        """

        Args:
            ozExe (str)
            environ (dict): normally oz.environ but can also be an arbitrary dict-like object

        Returns:
            OzCmdLine:
        """
        ozArea = environ.get('OZ_CONTEXT', '/') if environ else '/'
        using = environ.get('OZ_USING', '') if environ else ''
        if using == ozArea:
            using = ''
        if ozArea == '/':
            using = ''
        paks = environ.get('OZ_PAK_ADD', '') if environ else ''
        paksToAdd = paks.split(':') if paks else None
        return OzCmdLine(ozExe=ozExe, ozArea=ozArea, using=using, paksToAdd=paksToAdd)

    def toStr(self, useEval=False):
        cmdLine = self.ozExe
        cmdLine += ' {}'.format(self.ozArea)
        if self.using:
            cmdLine += ' --using {}'.format(self.using)
        for pak_ in self.paksToAdd:
            cmdLine += ' --add {}'.format(pak_)
        if useEval:
            cmdLine = 'eval `{}`'.format(cmdLine)
        return cmdLine

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__


class OzEnv(object):

    def __init__(self):
        self.cmd = OzCmdLine()

    @classmethod
    def fromFixture(cls, fixture):
        ins = cls()
        cmd_ = cls._createCmdFromEnviron(fixture)
        if cmd_ is None:
            cmd_ = cls._createCmdFromArguments(fixture)
        ins.cmd = cmd_
        return ins

    @classmethod
    def _createCmdFromEnviron(cls, fixture):
        if fixture.getValue('useCurrentEnvironment'):
            return OzCmdLine.createFromEnviron(ozExe=fixture.getValue('ozExe'), environ=os.environ)
        return None

    @classmethod
    def _createCmdFromArguments(cls, fixture):
        paksToAdd = fixture.getValue('paksToAdd') or []
        for p_ in paksToAdd:
            if p_.startswith('accTest-'):
                break
        else:
            paksToAdd.append(resources.currentPak())
        return OzCmdLine(
            ozExe=fixture.getValue('ozExe'),
            ozArea=fixture.getValue('ozArea') or '/',
            using=fixture.getValue('using') or '',
            paksToAdd=paksToAdd
        )

    def __eq__(self, other):
        return self.cmd == other.cmd

    def __ne__(self, other):
        return self.cmd != other.cmd

    def __hash__(self):
        return hash(self.cmd.toStr())

    def createProcess(self, cmdLine):
        cmdToRun = self.cmd.toStr(useEval=True)
        cmdToRun += ';{}'.format(cmdLine)
        logger.info('Creating process using command line (shell=True):\n{}'.format(cmdToRun))
        p = subprocess.Popen(cmdToRun,
                             shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p

    def createOzCmdLineOnly(self):
        cmdToRun = self.cmd.toStr(useEval=True)
        return cmdToRun


def fixtureIndexesByEnv(fixtures):
    """
    Group the fixtures by their oz environment;

    Args:
        fixtures (list):

    Returns:
        dict: a dictionary map the oz env object to a list of indexes; those indexes can be passed to the parse() method
    """
    idxDict = dict()
    for idx_, f_ in enumerate(fixtures):
        env_ = OzEnv.fromFixture(f_)
        idxList = idxDict.get(env_, list())
        idxList.append(idx_)
        idxDict[env_] = idxList
    return idxDict
