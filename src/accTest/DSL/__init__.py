"""
Interface: to hide irrelevant details behind abstraction.

-- GOF
"""


import parser as __parser

from accTest import terminal


def parse(dslFilePath, indexes=None, instantiation=True):
    fixtures = __parser.Parser().parse(dslFilePath, indexes=indexes)
    if not sum([len(f_.getTasks()) for f_ in fixtures]):
        terminal.printC('No tasks defined', color='red')
        return []
    if instantiation:
        for f_ in fixtures:
            instantiate(f_)
    return fixtures


def instantiate(fixture):
    tasks = fixture.getTasks()
    for taskName, taskOrProxy in tasks.iteritems():
        if not getattr(taskOrProxy, 'run', None):
            fixture.addTask(taskOrProxy.instantiate())
