# Bytewax

[![Actions Status](https://github.com/bytewax/bytewax/CI/badge.svg)](https://github.com/bytewax/bytewax/actions)
[![PyPI](https://img.shields.io/pypi/v/bytewax.svg?style=flat-square)](https://pypi.org/project/bytewax/)
[![Bytewax User Guide](https://img.shields.io/badge/user-guide-brightgreen?style=flat-square)](https://docs.bytewax.io/)

Bytewax is an open source Python framework for building highly scalable dataflows.

Bytewax uses [PyO3](https://github.com/PyO3/pyo3/) to provide Python bindings to the [Timely Dataflow](https://timelydataflow.github.io/timely-dataflow/) Rust library.

## Usage

Install the [latest release](https://github.com/bytewax/bytewax/releases/latest) with pip:

```shell
pip install bytewax
```

## Example

Here is an example of a simple dataflow program using Bytewax:

``` python
from bytewax import Executor

ec = Executor()
flow = ec.Dataflow(enumerate(range(10)))
flow.map(lambda x: x * x)
flow.inspect(print)


if __name__ == "__main__":
    ec.build_and_run()
```

Running the program:

``` bash
python ./pyexamples/wordcount.py
0
1
4
9
16
25
36
49
81
64
```

For a more complete example, and documentation on the available operators, check out the [User Guide](https://docs.bytewax.io/).

## License

Bytewax is licensed under the [Apache-2.0](https://opensource.org/licenses/APACHE-2.0) license.
