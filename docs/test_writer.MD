Write pipeline tests
--------------------

### Structure of a dsl file ###

Each dsl file consists of global properties and scopes in the form of Python global variables and classes;

Scopes (classes) may define scoped variables in the form of class variables;

### Rule of thumb ###

All properties (variables), either global or scoped, must be of **Python primitive types**, in another word, they **can not** be
 instances of user defined classes.

:point_right: think about the dsl file as an advanced json or xml document but just happens to be written in Python syntax

:grey_exclamation: Importing modules in the dsl file that are not part of Python's standard library is discouraged, unless the module comes
from accTest package itself, because there is no guarantee that
these modules are importable when the dsl file is parsed.
Imported modules must be aliased with leading double underscore to avoid confusing the dsl parser.

```python
from accTest import resources as __resources
```

Similarly, avoid defining functions in dsl file unless it is absolutely necessary. Again please use leading underscore to
  mark these callable "invisible" to the dsl parser.

```python
def __someFunction():
    ...
```

By default all global properties are "inherited" by each scope (a new copy with the same value is created in each scope).

```python
var = 10

class FooBar(object):
    pass  # "inherit" var by creating a scoped var whose value is 10
```

Scope can also choose to override the property

```python
var = 10

class FooBar(object):
    var = 20  # creating a scoped var whose value is 20
```

### Relationship between dsl file and test fixture ###

At runtime, AccTest's dsl parser iterates over the scopes and creates one **test fixture** for each scope (class);

The test fixture is functionally equivalent to ```unittest.TestCase``` for it is holding all the properties and tasks
 to be executed.

:point_right: Try to create and execute a minimalist dsl file

```python
class TestNothing(object):
    pass
```

Save this file to /tmp/testNothing.py, then execute it using accTest (note that file extension is not necessary in the
 command line as accTest automatically adds .py extension to the file name if no extension is found)

```
cd /tmp
accTest testNothing
```

AccTest creates the minimalist environment and throws a warning saying there is no tasks to execute.

```
No tasks defined.
```

If you get to this far, Congrad! The next step is to have the test actually do something

Please see the Examples and War Stories sections for some working examples.
