Example: Implementing publish test
----------------------------------

### The goal ###

A hypothetical pipeline produces a type of data called
"CharMap", which is stored as an ascii text file, with ".cm" suffix.

It is created by department A's pipeline tool and is productized via athena
product handler so that downstream departments can pick it up.

A test writer is given a task to create an automated test that
exercises the creation and publishing of this file.


### Create the dsl file ###

The test writer decides to create the dsl first - after all it is
a human readable file that shows what exactly this test is going to do.
It's a live document.

The dsl file can be found here:

```
$ACCEXAMPLES/taskExample.py
```

As the content shows, it declares a test fixture that
performances some to-be-implemented tasks, in a testing environment.
Not very exciting.

Try: copy the contents of this file to your dsl file: /tmp/examples/taskExample.py (or any other file path you'd prefer)

Now execute your dsl file - oops AccTest throws out an error:

```
accTest.exceptions.CanNotLoadTask: Search path: /tmp/examples/taskExample.py, Task: GenerateCharMap
```

That's right! The task has not been implemented yet (it is only declared in the dsl file), so the next step is to create
the physical implementation file.

### Create the implementation file ###

##### Create the first task class: GenerateCharMap

Firstly, create the placeholders:

```
mkdir /tmp/examples/taskExample
touch /tmp/examples/taskExample/GenerateCharMap.py
```

Then create the class ```GenerateCharMap``` and have it do nothing but fail straightaway

```python
from accTest.objectModel import baseTask

class GenerateCharMap(baseTask.BaseTask):

    def _run(self):
        return self.fatal('not implemented')
```

Now if execute the dsl again, we should see AccTest creates and enters the bubbled environment, instantiates the task
 then...... throws out an error - as we have designed - saying the task is not implemented.

We know our testing environment is correctly constructed and task executed. This is a good start! Let's begin to
import our production code, call some functions and verify the outputs.

See the fully implemented task in ```$ACCEXAMPLES/taskExample/GenerateCharMap.py```

This way of writing tests (as well as writing production code) is known as "incremental development". This method
suggests that changes are introduced progressively, incrementally in short iterations, while at the end of each
iteration, the developer should test-drive the whole system to get timely feedback.

##### Book keep state between task

One can consider the relationship between test fixture and task as a variation of OOP.

In OOP there are objects and their methods. Different methods of the same object can share state - provided that there
 is some kind of synchronization mechanism to prevent racing condition, or use the default single-threaded execution model

For example the logic of a method ```second()```
depends on an instance variable ```var``` that is populated or altered by method ```first()```, e.g.

```python
class Something(object):

    def first(self):
        self.var = 10

    def second(self):
        if self.var > 10:
            # do something...
        else:
            # do another something
```

AccTest provides a similar mechanism, allowing tasks to set properties on the fixture at runtime so that other tasks
 of the same fixture can make use of these data.

In the example here, task ```GenerateCharMap``` populates a property ```filePath``` on the fixture, which is retrieved
by the subsequent task ```PublishCharMap```.

At the time of writing, AccTest does not offer native assertion mechanism, which means that one must write Assertion
tasks as demonstrated in the example. Such Assertion task use fatal() or success() to report to the fixture.
