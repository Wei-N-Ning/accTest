AccTest Project Structure
-------------------------

(this page is under developement)

Project structure:

```
accTest/
      ./bin        # executables (exposed via PATH env var)
      ./docs       # markdown document files
      ./examples   # pre-generated example files (dsl and task implementations)
      ./resources  # non-code resource files (config etc.)
      ./src        # Python source code
      ./tests      # unit & integration tests
```

Source structure:

```
accTest/src
          ./DSL            # classes for dsl file and parser
          ./LOGGING        # as name suggests
          ./_testing       # * non production code, used by unit & integration tests only
          ./applications   # invoked by various executables
          ./execution      # how to execute the tasks; provides different execution models (local, remote)
          ./objectModel    # task and fixture; NOT including the execution logic
          ./shareable      # * may disappear in future major release; to store shareable tasks
          ./constants.py   # ..
          ./exceptions.py  # ..
          ./networks.py    # encapsulates network/socket operations; simplifies message-passing for execution classes
          ./resources.py   # provides a way to retrieve the resource file path: resources.filePath()
          ./terminal.py    # provides print-in-color function and other misc shell-related functions
```


