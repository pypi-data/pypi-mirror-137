import logging

from toscaparser.tosca_template import ToscaTemplate
from toscaparser.common.exception import ValidationError as TOSCAParserError
from yaml.error import YAMLError

from micadoparser import validator
from micadoparser.exceptions import ValidationError
from micadoparser.utils.csar import handle_csar
from micadoparser.utils.yaml import handle_yaml
from micadoparser.utils.utils import resolve_get_functions

logger = logging.getLogger("micadoparser." + __name__)


def set_template(path, parsed_params=None):
    """Parses any ADT and returns a ToscaTemplate

    :params: path, parsed_params
    :type: string, dictionary
    :return: template

    | parsed_params: dictionary containing the input to change
    | path: local or remote path to the file to parse
    """
    errors = None
    if path.endswith(".csar"):
        template = handle_csar(path, parsed_params)
    else:
        template = handle_yaml(path, parsed_params)

    validator.validation(template)
    _find_other_inputs(template)

    return template


def get_template(path, parsed_params):
    """Return a ToscaTemplate object

    Args:
        path (string): path to the saved ADT
        parsed_params (dict): tosca inputs

    Raises:
        ValueError: If the tosca-parser has trouble parsing

    Returns:
        ToscaTemplate: Parsed template object
    """

    error = ""
    try:
        template = ToscaTemplate(
            path=path, parsed_params=parsed_params, a_file=True
        )
    except TOSCAParserError as e:
        error = [
            line
            for line in e.message.splitlines()
            if all([line, not line.startswith("\t\t")])
        ]
        error = "\n".join(error)
    except AttributeError as e:
        error = f"{e}\n HINT: This might be due to a wrong type - check your imports."
    except YAMLError as e:
        error = f"YAML Error\n  {e}"
    except Exception as e:
        error = (
            f"Unknown Error:\n {e}\n\n"
            "Please raise a ticket at https://github.com/micado-scale/ansible-micado/issues."
        )

    if error:
        raise ValidationError(error, "TOSCA Parser could not parse the ADT...")

    return template


def _find_other_inputs(template):
    """Find `get_input` tags in the template, then resolve and update"""
    resolve_get_functions(
        template.tpl,
        "get_input",
        lambda x: x is not None,
        _get_input_value,
        template,
    )
    # Update nodetemplate properties
    for node in template.nodetemplates:
        node._properties = node._create_properties()


def _get_input_value(key, template):
    """Custom get_input resolution using parsed_params"""
    try:
        return template.parsed_params[key]
    except (KeyError, TypeError):
        logger.debug(f"Input '{key}' not given, using default")

    try:
        return [
            param.default for param in template.inputs if param.name == key
        ][0]
    except IndexError:
        logger.error(f"Input '{key}' has no default")
