"Big Four"
----------

Like other rnd teams, motion rnd manages a large number of software projects. Among them are
[mocore](https://gitlab.wetafx.co.nz/motion/mocore),
[motils](https://gitlab.wetafx.co.nz/motion/motils),
[motools](https://gitlab.wetafx.co.nz/motion/motools), and
[molibs](https://gitlab.wetafx.co.nz/motion/molibs), which the developers jokingly refer to as the "Big Four".

These four projects earned this title not just because of their size (100k+ source lines per project) but also because of
 circular dependencies as well as various types of anti-patterns they exhibited. They are difficult to maintain, to
  modify and deploy.

It usually takes one or more developers almost a week to fully deploy and test their releases. During testing, the
 developer would repeatedly run the following tasks:

- start a shell, oz-into a test shot
- launch Maya then launch the animation software (Chronos)
- run import-export round tripping tests on a hero character, a prop and some project-specific assets
- if an error or segfault is encountered, debug and fix it
- drink coffee and get back to step 1

Just like the good old CI idiom says: **if it is painful to do something, automate it and do it more often.** some motion
rnd developers come up with the initial idea of automating such pipeline tests.


Pipeline Tests vs Unit Tests
----------------------------

Interestingly, most motion rnd projects DO HAVE reasonable unit test and integration test coverage. The former uses
extensive mocking to test against **fake data** and **stub services** whereas the latter uses data normally copied from
production and special dev-version services.

While these isolated tests are quite good at catching local coding errors and bugs, they are not quite efficient in
catching inter-package communication issues, or the so-called **contract violation** issues.

One typical contract violation is that some one changes the class, method or function name in a library without updating the
call sites in the application (yes, you would argue that the library developer should release a major version and use
 the golden semantic version range on the application side to ensure compatibility...... you are quite right, but it's not
 easy to enforce such rule, particularly when some existing legacy practices forbid that).

In some other cases the violation could be less obvious, such as changing the Python function return type or introducing
 a new exception type unbeknown to the client (thus not handled properly).

Usually this type of mistakes are caught when the new versions have been deployed in the production environment, which
is too late for the testing game.

We could have saved ourselves and our clients, had we have a chance to automatically do:

- pick a production-like environment,
- oz-add our newly released library pak (which is not part of production environment yet)
- run the application(s) which depends on the library pak
- catch any error

This is what AccTest framework can offer.
