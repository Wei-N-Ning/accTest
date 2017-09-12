Search Paths
------------

AccTest expects the following directory structure:

```
name.py
name/
   ./Task1.py
   ./Task2.py
   ./Task3.py
   ......
```

```name.py``` - the dsl file

```name``` - the directory where tasks are implemented, named after the dsl file without extension

```name/Task1.py``` - the task implementation file


Task Implementation
-------------------

### task name ###

AccTest expects that each task is implemented in a class (e.g. Task1) which is located inside a python module with
the same name (e.g. Task1.py)

```python
# content of Task1.py
from accTest.objectModel import baseTask

class Task1(baseTask.BaseTask):
    def _run(self):
        return self.fatal('not implemented')
```

### requirements ###

AccTest requires each task implementation to inherit a common base class, defined in ```accTest.objectModel.baseTask```,
 and re-implement the ```_run()``` private method.

This method must return an instance of ```accTest.objectModel.result.Result```.

There are two convenient methods that create the result object in one call:

```python
success()  # optional message
fatal('')  # compulsory message
```

```fatal()``` requires a mandatory string argument to document the details of the error

### termination ###

By default, a failing task won't stop the process from executing they remaining tasks, but one can notify the fixture
  in the case of early-termination:

```python
class Task1(baseTask.BaseTask):

    def _run(self):
        fixture = self.getFixture()
        if ...  # some critical error
            fixture.terminate()  # notify the fixture
            return self.fatal('Task fails with critical error.')
        else:
            return self.success()
```

This will cause AccTest to skip the current fixture and move on to the next one (if any).

### API developers: release and deployment ###

At the time of writing, one needs **meDevTools-1.7.1+ digiwaflib-0.12.6+** to deploy accTest.

:grey_exclamation: All deployment operations require that your local repository has no uncommitted changes.

#### create local-pak (not to deploy but pointing to source code; pak is marked experimental and development)

```
oz / --add meDevTools-1.7.1 --add digiwaflib-0.12.6
cd accTest
./deploy local
```

#### create test-pak (deploy and point to /digi/test/$USER; pak is marked experimental and development)

:grey_exclamation: This can be done only when you have checked out a **non-master branch**:

```
oz / --add meDevTools-1.7.1 --add digiwaflib-0.12.6
cd accTest
./deploy $arg
```

$arg is optional, if provided the it will be the **pak version**, if not the pak version is the **name of the branch**

#### deploy production-pak (deploy and point to /digi/app)

create a local-pak first following the above step, then add the local pak to your oz environment:

```
oz / --add accTest-$USER.local --add meDevTools-1.7.1  add digiwaflib-0.12.6
cd accTest
./deploy $arg
```

$arg is optional, if not given a incremental patch version is deployed;
available choices are: "mi" and "ma" (minor increment or major increment)
