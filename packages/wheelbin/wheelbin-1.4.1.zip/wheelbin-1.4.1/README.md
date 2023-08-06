# wheelbin

`wheelbin` receives a wheel file and returns its compiled version,
i.e. an equivalent wheel file with the Python files substituted with
their corresponding Python bytecode files.

The output wheel filename reflects this compilation by fixing the Python
implementation, ABI and target architecture, and it replaces the
`.whl` extension with `.bin.whl`.

Additionally, Python files can be excluded from compilation by passing a
wildcard expression to the `--exclude` option.

`wheelbin` is a package forked from the original [`pycwheel`] by
Grant Patten.

## Usage

For example, given a wheel file `your_wheel-1.0.0-py3-none-any.whl`
and `wheelbin` installed on a GNU/Linux distribution under Python 3.7:

```sh
$ wheelbin your_wheel-1.0.0-py3-none-any.whl
# Output: your_wheel-1.0.0-cp37-cp37m-linux_x86_64.bin.whl
```


[`pycwheel`]:
https://github.com/grantpatten/pycwheel
