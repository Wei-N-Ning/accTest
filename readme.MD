(Acc)eptance (Test)ing Framework
================================


Summary
-------

**AccTest** is a lightweight Python testing framework to create high level pipeline acceptance tests.

**In a nutshell**, AccTest launches one or more processes that execute certain pipeline tasks in their designated oz
environments, then reports the result to the user.

Traditionally it is a human tester's job to run the pipeline software and report any error to the dev team;
Sometime software developers would test-drive the software themselves before urgent release (hot fixes);
In both cases the
testers or developers need to play the role of end user, running the software following certain staged scenarios, in a
production-like environment.
In a large scale vfx pipeline these tasks can be very time consuming (anti-costeffective) and unable to capture all the
 subtle inter-software issues.

See this article for [the original problem that inspired the creation of AccTest](docs/pre_acc_test.MD)

#### Language Support ####

The Subject-Under-Test can be written in any language.

#### Similarity to Continuous Integration pattern ####

The testing logic is defined in a .py configuration file (called a "dsl file" in the document and API), which specifies the oz
 environment, some contextual properties and the testing tasks to perform.

Testing tasks are executed in a bubbled environment either locally or on a remote host.

Results are published for continuous monitoring.

#### Similarity to xUnit pattern ####

Test fixtures are independent to each other.

Each test fixture is expected to follow the AAA or Triple-A idiom (Arrange-Act-Assert).

It offers fast feedback, particularly when a testing task fails (it can choose to stop all remaining tests or continue).

It has built-in support for source coverage measurement (powered by moTest).


Users' References
-----------------

Please read [conventions](docs/conventions.MD) first.

How to [invoke AccTest](docs/test_runner.MD) locally or remotely.

How to [write tests](docs/test_writer.MD)

How to [extend AccTest](docs/api_extension.MD)


Examples and War Stories
------------------------

[Example - A simple DSL file](docs/example_create_dsl.MD)

[Example - More sophisticated pipeline tests](docs/example_create_tasks.MD)

[War Story - Testing application logic using UI driver](docs/war_story_ui_driver.MD)

[War Story - Testing pipeline IO logic using Kenobi driver](docs/war_story_kenobi_driver.MD)


Requirements and Availability
-----------------------------

The minimal requirements are Python2.7+, network connection, oz (version 5) and moTest.


