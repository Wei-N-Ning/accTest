Example: hello world dsl
------------------------

AccTest provides some examples to illustrate its test writing workflow:

```
oz / --add accTest-0.2.0
cp -rf $ACCEXAMPLES /tmp/.
```

Find and open ```/tmp/examples/dslExamples.py``` in a text editor.

### define your test runtime environment ###

The first section in dslExample.py defines how to construct the runtime environment for the tests:

```python
ozArea = '/weta/shots/test/GEN'
paksToAdd = []
using = '/weta/testing/wip_paks'
```

To fluent oz users these concepts should be quite familiar. If not please refer to the official oz (version 5) document.

### override test runtime environment per fixture ###

As explained in the previous chapters, one can override a globally defined property inside a scope, so if a test
fixture must run in an environment different from the one defined globally, it is just a matter of adding a class
variable as shown in the class ```TestModifyKeyframesElementMotion```:

```python
class TestModifyKeyframesElementMotion(object):

    ozArea = '/weta/dev/GEN/base'  # running this test in a different oz environment
    productType = 'elementMotion'
    productName = 'fireball01'

    ...
```

AccTest will recognize that TestModifyKeyframesElementMotion requires a different environment therefore it creates
a separate bubble-environment for this fixture.

Once executed, AccTest reports two processes being created, each with its own environment and fixtures

```
INFO:accTest.execution.ozEnv:Creating process using command line (shell=True):
.../weta/shots/test/GEN
...
INFO:accTest.execution.ozEnv:Creating process using command line (shell=True):
.../weta/dev/GEN/base
...
```

### declare the testing tasks ###

In the dsl file, task name are "declared" in the class variable "tasks", which holds a list of strings as shown below:

```python
    tasks = [
        'DemoImportElement',
        'DemoExportElement',
        'DemoAssertElementExists'
    ]
```

At runtime, once the execution logic enters the bubbled environment, AccTest imports the task implementation files and instantiates 
the task classes. It then proceeds to call the run() public method from each task instances, collecting the subsequent results.

This characteristic - separating task "declaration" and task definition - has two benefits:

- Test writers are free to import any 3rd party modules in the task implementation files (being these are maya.cmds, 
nuke or athena, atlas, redbox....), provided that the bubble environment offers the required libraries or paks

- Test writers can leave the job of fully implementing the testing logic till the last minute, meaning that they can focus on 
organizing the test fixture, declaring the sequence of tasks before digging into the implementation details

See the next chapter for more details about task implementation


### provide the physical task implementation file ###

As the previous chapter explained, AccTest strictly requires that task and implementation file uses the same name.

In the case of dslExample, ```TestImportExportBodyMotion``` declares a task called ```DemoImportElement```, which is implemented 
in dslExample/DemoImportElement.py 

Here is a line-by-line explanation for this file:

```python
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

```
 
- import any 3rd party modules as you wish; make sure the oz area and paksToAdd provide these dependencies
- re-implement _run() private method
- do not re-implement the run() public method as there are complex error handling in the base class
- setting self.executed = True is unnecessary; it is just to demonstrate that the test has done something
- similarly re-implement the constructor is unnecessary; the default constructor does all the jobs
- to terminate the current fixture, call self.getFixture().terminate()
- you may have any number of classes or functions in this module

Once the file is created, executing the dsl file will produce some colorful shell messages 
