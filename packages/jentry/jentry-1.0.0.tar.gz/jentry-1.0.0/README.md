# jentry 

[![PyPI](https://img.shields.io/pypi/v/jentry)](https://pypi.org/project/jentry/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jentry)](https://pypi.org/project/jentry/)
![Loc](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/b35c243eb9fdbc51cdf51ac2770250e2/raw/loc.json)
![Comments](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/b35c243eb9fdbc51cdf51ac2770250e2/raw/comments.json)

[![Docs Deploy](https://github.com/HansBug/jentry/workflows/Docs%20Deploy/badge.svg)](https://github.com/HansBug/jentry/actions?query=workflow%3A%22Docs+Deploy%22)
[![Code Test](https://github.com/HansBug/jentry/workflows/Code%20Test/badge.svg)](https://github.com/HansBug/jentry/actions?query=workflow%3A%22Code+Test%22)
[![Badge Creation](https://github.com/HansBug/jentry/workflows/Badge%20Creation/badge.svg)](https://github.com/HansBug/jentry/actions?query=workflow%3A%22Badge+Creation%22)
[![Package Release](https://github.com/HansBug/jentry/workflows/Package%20Release/badge.svg)](https://github.com/HansBug/jentry/actions?query=workflow%3A%22Package+Release%22)
[![codecov](https://codecov.io/gh/HansBug/jentry/branch/main/graph/badge.svg?token=XJVDP4EFAT)](https://codecov.io/gh/HansBug/jentry)

[![GitHub stars](https://img.shields.io/github/stars/HansBug/jentry)](https://github.com/HansBug/jentry/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/HansBug/jentry)](https://github.com/HansBug/jentry/network)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/HansBug/jentry)
[![GitHub issues](https://img.shields.io/github/issues/HansBug/jentry)](https://github.com/HansBug/jentry/issues)
[![GitHub pulls](https://img.shields.io/github/issues-pr/HansBug/jentry)](https://github.com/HansBug/jentry/pulls)
[![Contributors](https://img.shields.io/github/contributors/HansBug/jentry)](https://github.com/HansBug/jentry/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/HansBug/jentry)](https://github.com/HansBug/jentry/blob/master/LICENSE)


A simple tools to get the entries of a java projects, based on [javalang](https://github.com/c2nes/javalang) library.

## Installation

You can simply install it with `pip` command line from the official PyPI site.

```
pip install jentry
```

For more information about installation, you can refer to the [installation guide](https://hansbug.github.io/jentry/main/tutorials/installation/index.html).

## Quick Start

### Use with CLI

You can directly use `jentry` CLI to get the entry of a java project. Such as the command below

```bash
jentry demo
```

The output should be like as shown follow (in this project, we have 2 different entries)

```
Main
homework.Main
```



### Only Use One Entry

You can get exactly one entry with `-F` command

```bash
jentry -F demo
```

The output should be

```
Main
```

This command can be used when you are trying to run a compiled java project, like this

```bash
java -cp target:${CLASSPATH} $(jentry -F demo)
```

The entry it found will be applied into the `java` command line.



### Pretty Print Entry

Actually, these entries can be printed with prettier ways, such as json and table.

```bash
jentry -f json demo
```

The json-formatted output.

```json
[
    {
        "entrance": "Main",
        "package": null,
        "class": "Main",
        "file": "demo/2018_spring_16061104_10/src/Main.java"
    },
    {
        "entrance": "homework.Main",
        "package": "homework",
        "class": "Main",
        "file": "demo/oo_course_2019_17373331_homework_2/src/homework/Main.java"
    }
]
```

And if the `-f` option is assigned to `table`

```bash
jentry -f table demo
```

A table with all the entries will be placed together.

```
+---------------+----------+-------+----------------------------------------------------------------+
|     Entry     | Package  | Class |                            Filename                            |
+---------------+----------+-------+----------------------------------------------------------------+
|      Main     |  <none>  |  Main |           demo/2018_spring_16061104_10/src/Main.java           |
| homework.Main | homework |  Main | demo/oo_course_2019_17373331_homework_2/src/homework/Main.java |
+---------------+----------+-------+----------------------------------------------------------------+
```



### Others 

Other features can be found in the help information, which can be displayed with `-h` option.

```bash
jentry -h
```

```
Usage: jentry [OPTIONS] [SOURCES]...

  Jentry - find the entry of your java project.

Options:
  -v, --version                   Show package's version information.
  -f, --format [table|json|entry]
                                  The format to display the entries  [default:
                                  entry]
  -s, --sorted_by [file|package|class|entry]
                                  The order to sorted by.  [default: file]
  -r, --reverse                   Reverse the sorted result, only applied when
                                  -s is used.  [default: False]
  -F, --first_only                Only show the first entry.  [default: False]
  -h, --help                      Show this message and exit.
```



### Use with Python

`jentry` can be imported into python

```python
from jentry.entry.script import load_entries_from_project

if __name__ == '__main__':
    for entry in load_entries_from_project('demo'):
        print(repr(entry))

```

The output should be

```
<JavaEntry class: Main, filename: 'demo/2018_spring_16061104_10/src/Main.java'>
<JavaEntry class: homework.Main, filename: 'demo/oo_course_2019_17373331_homework_2/src/homework/Main.java'>
```




## License

`jentry` released under the Apache 2.0 license.
