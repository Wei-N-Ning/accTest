"""
A DSL document should have NO dependencies (imports) to non-standard modules (as of Python2.7)
"""

# global properties, by default inherited by all test fixtures
ozArea = '/weta/shots/test/GEN'
hydraGroup = '/hft/shots/test/GEN'
hostType = 'python'
foobar = 'foobar'
paksToAdd = []
using = '/weta/testing/wip_paks'


class TestImportExportBodyMotion(object):

    # test fixture properties shadows (or value-overrides) the global properties
    hydraGroup = '/hft/shots/fif/0110'
    productType = 'bodyMotion'
    productName = 'impME01'
    hostType = 'mayaDemo'

    # all tasks are expected to be defined in /dslExample sub-directory;
    # each task should be defined in its own source file, which is named after the task (case sensitive)
    # so DemoImportElement task should be defined as <class DemoImportElement> in ./dslExample/DemoImportElement.py
    tasks = [
        'DemoImportElement',
        'DemoExportElement',
        'DemoAssertElementExists'
    ]


class TestImportExportElementMotion(object):

    hydraGroup = '/hft/shots/bsd/0050'
    productType = 'elementMotion'
    productName = 'fireball01'
    hostType = 'mayaDemo'

    # if a task contains a dot-path prefix, it is to instruct the DSL that this task is defined in an importable
    # module. In this case DSL will firstly import this module (accTest.shareable.tasks) then locate
    # <class DemoSharedTask>
    tasks = [
        'DemoImportElement',
        'DemoSharedTask',
        'DemoExportElement',
        'DemoAssertKeyframesOnElement'
    ]


class TestModifyKeyframesElementMotion(object):

    ozArea = '/weta/dev/GEN/base'
    productType = 'elementMotion'
    productName = 'fireball01'
    hostType = 'mayaDemo'

    tasks = [
        'DemoImportElement',
        'DemoAddKeyframesOnElement',
        'DemoExportElement',
        'DemoAssertKeyframesOnElement'
    ]
