Run tests locally
-----------------

Firstly, oz-add the latest version of accTest into your environment (at the time of writing, accTest-0.2.0 is the
latest release)

For API developers please use your local-pak or test-pak.

```
oz / --add accTest-0.2.0
```

Copy the demo files to your local directory like /tmp:

```
cp -rf $ACCEXAMPLES /tmp/.
cd /tmp/examples
```

AccTest exposes an executable named "accTest" that has the following interfaces

```
accTest $dslName
accTest $protocol $dslName
```

```$dslName``` is the name of the Python configuration file.

```$protocol``` is an optional argument that specifies the execution methods. Here are the available choices

```
python / py: to execute the tasks with vanilla Python interpreter (equivalent to /usr/bin/env python)
mayapy: to execute the tasks with Maya standalone, pre-initialized (no need to call standalone.initialize())
maya: to execute the tasks inside Maya GUI, equivalent to running the tasks in Maya script editor
```

:point_right: Try to run this command in your shell ```accTest dslExample```


Run tests remotely
------------------

AccTest provides a tool that turns any workstation into dedicated testing machine.

### Start accSlave on a workstation ###

```
accSlave $port
```

Once acc slave is up and running, you should be able see the following message from the shell on the testing machine.

```
accSlave 1111
Waiting for connection (this: ('192.168.48.59', 1111))
```

It means the testing machine is ready to receive tasks sent by the master.

### Run tests on the testing machine ###

Tasks are sent to the testing machine via a command line tool called ```accSlaveRun```, which has the following
interface:

```
accSlaveRun $host $port $dslName
accSlaveRun $host $port $protocol $dslName
```

```$host```: the name of the workstation or its ip address

:point_right: One can play around accSlave and accSlaveRun on the same workstation; Try to launch accSlave on your
workstation, then call accSlaveRun from a different shell


Debug a test
------------

When a test fails it is important that we can quickly identify the cause and fix it. Use ```accDebug``` shell tool,
which has the same  interface as ```accTest```, to print out some helpful information, which includes the oz command
line and the shell command that executes the tasks.

You can then starts a new shell and re-run these commands with a debugger.

To debug Python code, **pudb** (pak name: **pypudb-2016.2**) is highly recommended.
