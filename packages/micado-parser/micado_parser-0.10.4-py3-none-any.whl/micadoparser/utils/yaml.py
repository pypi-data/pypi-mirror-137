"""
MiCADO Submission Engine YAML Utilities
---------------------------------------
Handles various aspects of YAML in parsing templates
"""

import logging
import urllib
from tempfile import NamedTemporaryFile
from pathlib import Path

from ruamel.yaml import YAML, representer

from micadoparser import parser
from micadoparser.utils import tosca

logger = logging.getLogger("micadoparser." + __name__)


class NonAliasingRTRepresenter(representer.RoundTripRepresenter):
    """Turn off auto-aliases in ruamel.yaml"""

    def ignore_aliases(self, _):
        return True


yaml = YAML()
yaml.default_flow_style = False
yaml.preserve_quotes = True
yaml.Representer = NonAliasingRTRepresenter


class YAMLLoader:
    """Load a template from file or URL

    Provides attributes for the YAML dict object and
    if a file path, the parent directory of the file
    """

    def __init__(self, path):
        self.parent_dir = None
        self.dict = self._get_tpl(path)

    def _get_tpl(self, path):
        """Return the template dictionary"""

        file_path = Path(path)

        if file_path.is_file():
            self.parent_dir = file_path.parent
            return get_yaml_data(file_path)

        # Otherwise try as a URL
        try:
            f = urllib.request.urlopen(path)
            return get_yaml_data(f, stream=True)
        except ValueError:
            logger.error(f"Could not find the ADT at {path}")
            raise FileNotFoundError(f"Could not find the ADT at {path}")
        except urllib.error.URLError as e:
            logger.error(f"Could not reach URL {e}")
            raise FileNotFoundError(f"Could not reach URL {e}")


def dump_order_yaml(data, path):
    """Dump the dictionary to a yaml file"""

    with open(path, "w") as file:
        yaml.dump(data, file)


def get_yaml_data(path, stream=False):
    """Retrieve the yaml dictionary form a yaml file and return it"""

    if stream:
        return yaml.load(path)

    with open(path, "r") as file:
        data = yaml.load(file)

    return data


def handle_yaml(path, parsed_params):
    """Handles YAML (single-file) ADTs and return the new path

    :params: path, parsed_params
    :type: string, dictionary
    :return: template

    | parsed_params: dictionary containing the input to change
    | path: local or remote path to the file to parse
    """

    tpl = YAMLLoader(path)

    if tosca.is_v1_3(tpl.dict):
        tosca.fix_version(tpl.dict)
        tosca.resolve_occurrences(tpl.dict, parsed_params)

    with NamedTemporaryFile(dir=tpl.parent_dir, suffix=".yaml") as temp_tpl:
        dump_order_yaml(tpl.dict, temp_tpl.name)
        template = parser.get_template(temp_tpl.name, parsed_params)

    return template
