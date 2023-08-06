# MiCADO Parser
The MiCADO component responsible for parsing and validating ADTs

Historically part of the [MiCADO TOSCASubmitter](https://github.com/micado-scale/component_submitter), now a standalone library and command-line tool used inside MiCADO and on its own for validating single-file (YAML) and multi-file (CSAR) ADTs.

## Dependencies
The MiCADO Parser uses the following packages:
- [TOSCA Parser](https://opendev.org/openstack/tosca-parser)
- [ruamel.yaml](https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree/)
- [Click](https://github.com/pallets/click)

## Installation
Install the latest version of the MiCADO Parser from PyPI.

```bash
pip install micado-parser
```

or from GitHub.

```bash
git clone https://github.com/micado-scale/micado-parser
pip install micado-parser/.
```

## Usage

### Command-line
For some helpful tips, use the `--help` option

```bash
micadoparser --help
```

To validate an ADT, simply point at an ADT.

```bash
micadoparser /home/ubuntu/adts/nginx.yaml
```

Multi-file ADTs in .csar format are also supported

```bash
micadoparser /home/ubuntu/adts/wordpress.csar
```

The tool can handle multiple files.

```bash
micadoparser ~/adts/nginx.yaml ~/adts/wordpress.csar
```

Or an entire directory.

```bash
micadoparser ~/adts/*
```

For verbose output use the `-v` option (for even more verbosity use `-vv` or `-vvv`).
```bash
micadoparser -v ~/adts/nginx.yaml
```

### Library
The primary function of the MiCADO Parser is to return a validated [ToscaTemplate](https://opendev.org/openstack/tosca-parser/src/branch/master/toscaparser/tosca_template.py) object.

To use it in your own project, simply import the `set_template` function and pass it the path to your ADT. You can optionally pass a dictionary of TOSCA inputs, if inputs are defined in your ADT.

```python
from micadoparser import set_template

tpl = set_template("/home/ubuntu/adts/nginx.yaml")

tpl_with_params = set_template(
    "home/ubuntu/adts/wordpress.csar",
    {"username": "jay", "token": "ABD992LOKAL"}
)
```

To use the package for validation only, use the `set_template` function and catch the `MultiError` exception.

```python
from micadoparser import set_template, MultiError

try:
    set_template("/home/ubuntu/adts/nginx.yaml")
except MultiError as e:
    print(e)
```

## Comparison with the OpenStack TOSCA Parser
The MiCADO Parser adds a few features compared to the upstream TOSCA Parser.
- MiCADO-specific validations
- MiCADO-specific CSAR handling
- Input resolution
- Support for some TOSCA v1.3 features