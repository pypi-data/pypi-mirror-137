# pyspj 

[![PyPI](https://img.shields.io/pypi/v/pyspj)](https://pypi.org/project/pyspj/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyspj)](https://pypi.org/project/pyspj/)
![Loc](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/20b3613a7b38335548c65f11f60e4a2d/raw/loc.json)
![Comments](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/20b3613a7b38335548c65f11f60e4a2d/raw/comments.json)

[![Docs Deploy](https://github.com/HansBug/pyspj/workflows/Docs%20Deploy/badge.svg)](https://github.com/HansBug/pyspj/actions?query=workflow%3A%22Docs+Deploy%22)
[![Code Test](https://github.com/HansBug/pyspj/workflows/Code%20Test/badge.svg)](https://github.com/HansBug/pyspj/actions?query=workflow%3A%22Code+Test%22)
[![Badge Creation](https://github.com/HansBug/pyspj/workflows/Badge%20Creation/badge.svg)](https://github.com/HansBug/pyspj/actions?query=workflow%3A%22Badge+Creation%22)
[![Package Release](https://github.com/HansBug/pyspj/workflows/Package%20Release/badge.svg)](https://github.com/HansBug/pyspj/actions?query=workflow%3A%22Package+Release%22)
[![codecov](https://codecov.io/gh/HansBug/pyspj/branch/main/graph/badge.svg?token=XJVDP4EFAT)](https://codecov.io/gh/HansBug/pyspj)

[![GitHub stars](https://img.shields.io/github/stars/HansBug/pyspj)](https://github.com/HansBug/pyspj/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/HansBug/pyspj)](https://github.com/HansBug/pyspj/network)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/HansBug/pyspj)
[![GitHub issues](https://img.shields.io/github/issues/HansBug/pyspj)](https://github.com/HansBug/pyspj/issues)
[![GitHub pulls](https://img.shields.io/github/issues-pr/HansBug/pyspj)](https://github.com/HansBug/pyspj/pulls)
[![Contributors](https://img.shields.io/github/contributors/HansBug/pyspj)](https://github.com/HansBug/pyspj/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/HansBug/pyspj)](https://github.com/HansBug/pyspj/blob/master/LICENSE)


A light-weighted special support utils.

## Installation

You can simply install it with `pip` command line from the official PyPI site.

```
pip install pyspj
```

For more information about installation, you can refer to the [installation guide](https://hansbug.github.io/pyspj/main/tutorials/installation/index.html).



## Quick Start

### Use with CLI

You can use `pyspj` CLI to judge the running result, the help information is as follows

```
Usage: pyspj [OPTIONS]

Options:
  -v, --version                   Show package's version information.
  -i, --input TEXT                Input content of special judge.
  -o, --output TEXT               Output content of special judge
  -I, --input_file FILE           Input file of special judge (if -i is given,
                                  this will be ignored).

  -O, --output_file FILE          Output file of special judge (if -o is
                                  given, this will be ignored).

  -t, --type [free|simple|continuity]
                                  Type of the final result.  [default: free]
  -s, --spj TEXT                  Special judge script to be used.  [required]
  -p, --pretty                    Use pretty mode to print json result.
  -h, --help                      Show this message and exit.
```

Here is a simple example, a spj file named`test_spj.py`

```python
import io


def spj_func(stdin: io.StringIO, stdout: io.StringIO):
    inputs = [int(item.strip()) for item in stdin.read().strip().split(' ') if item]
    _correct_sum = sum(inputs)

    outputs = stdout.read().strip().split(' ', maxsplit=2)
    if len(outputs) >= 1:
        _result = int(outputs[0])
    else:
        return False, 'No output found.'

    if _result == _correct_sum:
        return True, 'Correct result.', 'Oh yeah, well done ^_^.'
    else:
        return False, 'Result {correct} expected but {actual} found.'.format(
            correct=repr(_correct_sum), actual=repr(_result)
        )


__spj__ = spj_func

```

You can use CLI to judge the result

```shell
# input: 1 2 3 4 5
# output: 15
pyspj -i '1 2 3 4 5' -o '15' -s test_spj:spj_func
```

It means import special judge function `spj_func` from package `test_spj`, the output result should be

```
{"correctness": true, "detail": "Oh yeah, well done ^_^.", "message": "Correct result."}
```

Besides, a simpler command line can be used due to the definition of `__spj__` variable

```shell
pyspj -i '1 2 3 4 5' -o '15' -s test_spj
```

This command is equivalent to the above command.



### Input & Output from File

When the scale of input or output is huge, you can load them from `-I` and `-E` option.

Here is an exmaple, a input file named`test_input.txt`

```
1 2 3 4 5
```

Output file named`test_output.txt`

```
15
```

You can use CLI to judge the result in the txt files

```shell
pyspj -I test_input.txt -O test_output.txt -s test_spj
```

The output should be

```
{"correctness": true, "detail": "Oh yeah, well done ^_^.", "message": "Correct result."}
```

Actually, `-I` and `-o` can be used together, so are the `-i` and `-E` options. There will be nothing different.



### Pretty Json Output

If you need pretty print the result (especially when you are debugging), you can use `-p` option.

```shell
pyspj -i '1 2 3 4 5' -o '15' -s test_spj -p
```

The output should be

```json
{
    "correctness": true,
    "detail": "Oh yeah, well done ^_^.",
    "message": "Correct result."
}
```



### Additional Arguments

Sometimes, you can use additional arguments to support more complex cases.

Such as the special judge function below

```python
import io


def spj_func(stdin: io.StringIO, stdout: io.StringIO, fxxk=None):
    inputs = [int(item.strip()) for item in stdin.read().strip().split(' ') if item]
    _correct_sum = sum(inputs)

    if not fxxk:
        outputs = stdout.read().strip().split(' ', maxsplit=2)
        if len(outputs) >= 1:
            _result = int(outputs[0])
        else:
            return False, 'No output found.'

        if _result == _correct_sum:
            return True, 'Correct result.', 'Oh yeah, well done ^_^.'
        else:
            return False, 'Result {correct} expected but {actual} found.'.format(
                correct=repr(_correct_sum), actual=repr(_result)
            )
    else:
        return False, 'Result error because {value} detected in fxxk.'.format(value=repr(fxxk))


__spj__ = spj_func

```

An extra `fxxk` argument is used, so the following command line can be used to set the value of argument `fxxk` to `2` (string)

```shell
pyspj -i '1 2 3 4 5' -o '15' -s test_spj -p -V fxxk=2
```

The output should be

```
{
    "correctness": false,
    "detail": "Result error because '2' detected in fxxk.",
    "message": "Result error because '2' detected in fxxk."
}
```

ATTENTION:

* **Addtional argument should has a default value**, otherwise when the value is not provided by command line, it will raise error.
* **The default type of addtional arguments are string**, you need to convert it to the type you actually need in your special judge function.

### Use Special Judge in Python

`pyspj` can be used in native Python by importing package

```python
from pyspj import execute_spj_from_string

if __name__ == '__main__':
    result = execute_spj_from_string('test_spj', '1 2 3 4 5', '15')
    print(result.to_json())

```

The output should be

```
{'correctness': True, 'message': 'Correct result.', 'detail': 'Oh yeah, well done ^_^.'}
```

File input or file output are supported as well, like the following code

```python
from pyspj import execute_spj_from_file

if __name__ == '__main__':
    result = execute_spj_from_file('test_spj', 'test_input.txt', 'test_output.txt')
    print(result.to_json())

```

The output should be the same as the abovementioned code.

Addtional arguments are also supported like the CLI.

```python
import codecs
import io

from pyspj import execute_spj

if __name__ == '__main__':
    with codecs.open('test_input.txt') as stdin, \
            io.StringIO('15') as stdout:
        result = execute_spj('test_spj', stdin, stdout, arguments={'fxxk': 2})
    print(result.to_json())

```

The output should be

```
{'correctness': False, 'message': 'Result error because 2 detected in fxxk.', 'detail': 'Result error because 2 detected in fxxk.'}
```



### Make My Special Judge Runnable

You can add entry for your special judge function by using `pyspj_entry` function and call it in `__main___`

```python
import io

from pyspj import pyspj_entry


def spj_func(stdin: io.StringIO, stdout: io.StringIO):
    inputs = [int(item.strip()) for item in stdin.read().strip().split(' ') if item]
    _correct_sum = sum(inputs)

    outputs = stdout.read().strip().split(' ', maxsplit=2)
    if len(outputs) >= 1:
        _result = int(outputs[0])
    else:
        return False, 'No output found.'

    if _result == _correct_sum:
        return True, 'Correct result.', 'Oh yeah, well done ^_^.'
    else:
        return False, 'Result {correct} expected but {actual} found.'.format(
            correct=repr(_correct_sum), actual=repr(_result)
        )


if __name__ == '__main__':
    pyspj_entry('test_spj', spj_func, version='0.1.1')()

```

Save the code above to `test_spj.py`, and then you can run it like pyspj cli.

```shell
python test_spj.py -h
```

The output should be

```
Usage: test_spj.py [OPTIONS]

  Test_spj - test a pair of given input and output.

Options:
  -v, --version           Show special judge's version information.
  -i, --input TEXT        Input content of special judge.
  -o, --output TEXT       Output content of special judge
  -I, --input_file FILE   Input file of special judge (if -i is given, this
                          will be ignored).
  -O, --output_file FILE  Output file of special judge (if -o is given, this
                          will be ignored).
  -V, --value TEXT        Attached values for special judge (do not named as
                          "stdin" or "stdout").
  -p, --pretty            Use pretty mode to print json result.
  -h, --help              Show this message and exit.
```

And test the input

```shell
python test_spj.py -i '1 2 3 4 5' -o 15
```

```text
{"correctness": true, "detail": "Oh yeah, well done ^_^.", "message": "Correct result."}
```



Besides, if the target environment does not have python, you can build this script with [pyinstaller](https://github.com/pyinstaller/pyinstaller)

```shell
pip install pyspj[build]
pyinstaller -D -F -n test_spj -c test_spj.py
```

A standalone executable file will be created.

## License

`pyspj` released under the Apache 2.0 license.
