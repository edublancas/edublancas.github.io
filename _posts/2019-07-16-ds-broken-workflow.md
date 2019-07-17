---
layout: post
title: 5 signs your Data Science workflow is broken
comments: true
---

Developing reproducible data pipelines is hard, but before we even think about reproducibility your project has to meet some minimum standards. This post discusses some recurring bad practices when developing data pipelines and provides some advice to overcome them.

## 1. Lack of setup instructions

The first step for every software project is to get the environment up a running (e.g., install UNIX package A, then install Python 3.7, then install Python libraries X, Y and Z), however, more often than not, the environment is setup once and instructions are never recorded.

Data Science projects often depend on complex software setups (e.g., installing GPU or database drivers); lack of instructions will surely cause a lot of trouble for the team, especially when a new member joins or when the project is taken to a production environment.

This setup instructions have to be always up to date, they will break if a single new dependency is not registered and unnecessarily complex if any dependency is no longer needed.

**How to fix it?** All projects should come with a shell script to setup the project, package managers do the heavy lifting for installing software so you might assume that one is already installed.

To prevent setup instructions become outdated, test them every time your code changes by using a [Continuous Integration](Continuous Integration) service such as [Travis CI](https://travis-ci.org/). While CI services can detect when your dependencies no longer work, they cannot detect unnecessary libraries, those you have to remove manually from the setup script.

## 2. Environment configuration embedded in the source code

If you keep seeing this error message when running your pipeline:

```bash
"/Users/coworkersname/data/clean_v2.parquet" file not found.
```

It is probably because someone in the team hardcoded a path to a file/directory that only exists in their machine. Even if you are working in a shared filesystem, it is a good idea to keep files separate to prevent accidentally overwriting their work. **Explicit paths should never make it to the code.**

**How to fix it?** Keep all things such as I/O paths and host addresses in a separate place and read from there. For example, you might have a file like this in your project's root directory:

```yaml
# locations.yaml
data:
    # all raw data goes here
    raw: ~/project/data/raw/
    # all processed data goes here
    processed: ~/project/data/processed

# host to the database
db: db.organization.com:5421/database
```

Everyone then should treat that file as a *contract*: you must read and write only to these directories. Each member can customize their configuration file and nothing should break. Your code will look like this:

```python
from pathlib import Path

import pandas as pd
from my_project import locations


def clean_data():
    # load content of locations.yaml
    path_raw = locations['data']['raw']
    path_clean = locations['data']['processed']

    # read a file relative to the raw data folder...
    pd.read_parquet(Path(path_raw, 'dataset.parquet'))

    # clean the data...

    # write to a file relative to the clean data folder...
    pd.to_parquet(Path(path_clean, 'dataset.parquet'))
```

Make sure the file is easily discoverable inside your scripts, you might want to create a function that automatically finds a `locations.yaml` file in the current working directory or any parent folders up to certain levels and raises and `Exception` if it cannot find one.

## 3. End-to-end pipeline execution requires manual intervention

A pipeline is not such if it needs manual intervention to run. Given the raw data, you should be able to run the pipeline end-to-end with a single command. For starters, that means you should only use scripting tools such as Python or R, and no GUI tool such as Excel.

Automated execution is a prerequisite for automated testing. Bugs are inevitable, but automated testing can save you from finding those bugs in a production environment.

**How to fix it?** If setup instructions are provided and there are not hardcoded paths, having an automated pipeline will be easier. As with setup instructions, the only reliable way to keep this working is to include a shell script in the CI service to make sure your pipeline still runs. If you are working with large datasets, you may want to pass a sample of the data for testing purposes.

## 4. Intermediate results are shared over e-mail/cloud storage

A (unfortunate) common practice in many data analysis projects is to share intermediate results. Reasons vary but the pattern goes like this: member `A` updates some code in the pipeline that `B` needs as input, so `A` runs the updated code and shares the new results with `B`, who then uses this new file as input instead of the old version.

Sharing intermediate results is a terrible practice since it makes reproducibility harder. **Intermediate results should never be shared**, `A` should just push the new code and `B` should execute it to get the new input to use.

**How to fix it?** Fixing this pattern is harder, all previous sections are prerequisites for this one, namely:

1. There should a setup script to configure setup the environment
2. Configuration should be centralized in a single file, out of the source code
3. There should be a script to execute the pipeline end-to-end

If all those requisites are met, there is no need to share intermediate files.

The only situation when sharing intermediate files might be necessary is when any of your tasks either a) takes *a lot* to run or b) it has to be run in a restricted environment (e.g., a shared cluster). In such case, special care should be given to make sure that the code that produced some results is appropriately stored in version control. **Avoid this situation as much as possible.**

For most projects, this should not be the case. If you are working with large datasets, you probably already have some distributed infrastructure which makes your computationally heavy scripts run in a reasonable amount of time, if they do not, consider splitting them in smaller steps.


## 5. A change in a single step requires you to execute the pipeline end-to-end

During development, it is always the case that steps are revisited (added features, fixed bugs). Every time you make a change, you have to make sure that all changes propagate to steps downstream. Since steps in a data pipeline often take minutes or even hours to run, an update should only trigger execution on their downstream dependencies to avoid wasteful computations.

If there is no way for your pipeline to know which steps are affected by any given update you only have two choices: either to run the entire pipeline again or manually check which steps have to be run. Both options are a waste of your time.

**How to fix it?** There is not a single answer here. I have not found any library to easily fix this issue (I implemented my own solution but it is not publicly available yet). If all your processing is done locally, my recommendation is to use [Make](https://en.wikipedia.org/wiki/Make_(software)).

## Final comments

I hope this post helps you find areas for improvement in your data projects. Putting attention to this issues will pay off in the long run. A working workflow not only will increase your productivity to get your analysis right faster but will help you build more robust data products.


