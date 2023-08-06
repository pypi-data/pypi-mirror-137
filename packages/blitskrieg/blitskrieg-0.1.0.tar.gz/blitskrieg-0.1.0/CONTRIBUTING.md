# Contributing

Here's a brief list of areas where contributions are particularly welcome:
- adding new functionalities and expose them on the gRPC interface
- maintaining or extending the existing features
- security improvements
- testing and bugfixing

To get started, please consider discussing the change via issue, email or any
other method with the project owners.


## Linting

To check the code for common errors run:

```bash
$ ./unix_helper lint
```

This will check the code with [`pylint`](https://github.com/PyCQA/pylint).


## Formatting

To format the code we use [`yapf`](https://github.com/google/yapf) and
[`isort`](https://github.com/PyCQA/isort).

Run `git config core.hooksPath .githooks` in order to change the project git
hooks location. Doing so the format tools will be automatically called at
pre-commit time on staged files, leaving any formatting changes unstaged.

Otherwise, if you don't wish to activate the git hook, you can manually call
`./unix_helper format` from the project root directory. This will run the same
script called by the git hook.


## Merge Request Process

1. Rebase on develop for new features or master for fixes

1. Test and lint the code to make sure there are no regressions

1. Update the README.md with details about the introduced changes

1. Create the merge request


## Code of Conduct

This project adheres to No Code of Conduct. We are all adults.
We accept anyone's contributions. Nothing else matters.

For more information please visit the
[No Code of Conduct](https://github.com/domgetter/NCoC) homepage.
