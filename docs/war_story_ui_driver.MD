War Story: Testing Application Logic Using UI Driver
----------------------------------------------------

### UI test strategies

##### record-and-play strategy

Some advanced UI testing framework offers the ability to record the user input events (such as mouse-moves, mouse-clicks and key
strokes) and "replay" these events in a test to verify the behavior of the system.

Using this method, the tests can easily rehearse sophisticated user scenarios.

:point_right: Honorable mention: *squish testing framework*

The downside of record-and-play strategy is that, if any change to a UI component - no matter how trivial it is -
 affects the pre-recorded sequence of events, such as changing the name or position of a button, the test may fail even
 though the business logic stays unmodified.

##### ui-driver strategy

Another commonly used strategy sees the creation of a "middle man", known as ui-diver, that stands between the tests
and the UI system.

This middle man provides a simplified interface for the tests, such as:

```python
class UiDriver(object):

    def doFileSave(self):
        ...

    def doFileNew(self):
        ...

    def doEditCopy(self):
        ...

    def doEditPaste(self):
        ...
```

Tests that used to talk directly to the UI system would talk to the ui driver, so instead of accessing the UI
components directly as such:

```python
class TestUISystem(unittest.TestCase):

    def test_fileSave_expectFileCreated(self):
        ui = SuperComplexUI()

        # navigate through the object graphs and find the "save" button
        # skip 100+ lines here

        saveButton.click()

        self.assertFileCreated(filePath)
```

Now tests have the option to leave the complexity behind the ui driver as such:

```python
class TestUISystemWithDriver(unittest.TestCase):

    def test_fileSave_expectFileCreated(self):
        uiDriver = UiDriver(SuperComplexUI())
        filePath = uiDriver.doFileSave()
        self.assertFileCreated(filePath)
```

Any changes to the save button and related UI components only require the ui driver to update its doFileSave() method;
 The tests can stay unchanged.

In fact some good UI systems themselves can play the role of a middle man.

For instance, in order to test with an instance of ```QtGui.QTreeWidget```, one can instantiate this class and start
calling addTopLevelItem(), or resize(), without the overhead to initialize its drawing state, or to navigate through its
  internal object graph - they are all well encapsulated.

The downside is that, now the developers have to maintain two projects: the UI system and the UI driver.
