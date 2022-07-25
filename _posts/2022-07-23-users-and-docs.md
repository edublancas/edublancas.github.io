---
layout: post
title: Don't make users read your docs
comments: false
---

As an [open-source maintainer](https://github.com/ploomber/ploomber), I always put effort into documenting all known edge cases so that users know how to fix problems. So, whenever users report incompatibilities, we highlight them in our documentation. Still, I realized this approach wasn't working when users came to our Slack asking for help with problems we had already documented.

As project maintainers, we tend to be overly optimistic about how good the documentation is. But the target metric should not be how detailed our documentation is but how fast users can get things done. And when things go wrong, reading the documentation is not always the quickest route, so *don't make your users read your docs, help them right on the spot.*

## Motivating example

A few weeks ago, a user [reported an issue](https://github.com/ploomber/ploomber/issues/882). The details are not important, but it required us to add a new argument to a class. We added the argument to the constructor, documented it, and posted the solution in the GitHub issue; however, when thinking about what would happen if a new user had the same issue, I realized we solved the problem for one user but not the rest. Most likely, other users would have a hard time trying to fix the issue, and most likely, they'd give up if they didn't find the answer quickly.

## Useful error messages

A helpful error message tells you three things:

1. What failed
2. Why it failed
3. How to fix it

For example:

> RuntimeError: Cannot re-initialize CUDA in forked subprocess. To use CUDA with multiprocessing, you must use the 'spawn' start method

This error message contains the three elements:

1. Cannot re-initialize CUDA [What failed]
2. ...in forked process [Why it failed]
3. Use the 'spawn' start method [How to fix it]


The problem is that our framework builds an abstraction, so users don't have to use the `multiprocessing` module directly; hence, the user couldn't fix the issue unless they modified the source code.

In our specific use case, here's a better error message:

> RuntimeError: Cannot re-initialize CUDA in forked subprocess. To use CUDA with multiprocessing, Pass 'spawn' to the 'start_method' argument of the Parallel executor constructor

Let's see how to achieve this.

## Helpful error messages

*Note: the following sections contain Python code snippets, but the idea applies to any language.*

We want to anticipate the error and tell the user how to get things running:

```python
from some_package.exceptions import SomeException

def thing_that_breaks(argument):
    ...


def thing_that_the_user_calls(argument):
    try:
        thing_that_breaks(argument=argument)
    except SomeException as e:
        # add more context and raise whatever exception type makes sense
        raise RuntimeError('How to fix it') from e
    except:
        # raise the original exception, unmodified
        raise
    ...
```

*Note:* the `raise exception from another_exception` expression is called a [chained exception](https://peps.python.org/pep-3134/) in Python.

The previous snippet will provide the user-specific instructions when encountering the problem using our software.

However, we're assuming that:

1. We can import `some_package.exceptions` in our project's codebase (which implies adding it as a dependency)
2. We are sure that when `SomeException` is raised, the solution is what we are displaying to the user

Sometimes exceptions are too general, so we need to dig deeper. In such cases, we can use the error message as a proxy:

```python
def thing_that_breaks(argument):
    ...


def thing_that_the_user_calls(argument):

    try:
        thing_that_breaks(argument=argument)
    except Exception as e:
        if 'some hint' in str(e):
            raise Exception('Instructions on how to fix it') from e
        else:
            raise
    ...
```

There are obvious drawbacks to this approach: the error message might change, although the same is true for the exception type, so in any case, ensure you have unit tests in place.

I've encountered cases where checking the error message isn't enough, and we might display inaccurate instructions. In such situations, I write an error to reflect that:

> If having issues with X, try [possible solution]

## The end

If you enjoyed this, let's connect on [Twitter](https://twitter.com/edublancas), where I often post my adventures as open-source maintainer, and if you do Data Science, check out our [project.](https://github.com/ploomber/ploomber)

