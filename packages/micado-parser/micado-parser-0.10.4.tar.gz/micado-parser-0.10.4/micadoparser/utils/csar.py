"""
MiCADO Submission Engine CSAR Utilities
---------------------------------------
Handles various aspects of CSARchives

Eg. Validate raw CSAR files (zip) by passing individual templates
to the YAML validator
"""

import os
import shutil
import tempfile
import zipfile

from micadoparser import parser
from micadoparser.utils.yaml import handle_yaml
from micadoparser.exceptions import MultiError, ValidationError


def handle_csar(path, parsed_params):
    """Handles CSAR (multi-file) ADTs and returns any errors caught
    :params: path, parsed_params
    :type: string, dictionary
    :return: template

    | parsed_params: dictionary containing the input to change
    | path: local or remote path to the file to parse
    """
    errors = csar_validation(path, parsed_params)
    if errors:
        raise MultiError(errors, "Cannot parse CSAR, issues in templates...")
        
    template = parser.get_template(path, parsed_params)

    return template


def csar_validation(file, parsed_params):
    """Validates individual YAML files inside a CSAR"""
    temp_dir = None
    errors = set()
    try:
        temp_dir = tempfile.NamedTemporaryFile().name
        with zipfile.ZipFile(file, "r") as zf:
            zf.extractall(temp_dir)
    except Exception as e:
        raise ValidationError("[CSAR] Could not extract CSARchive")

    for file in os.listdir(temp_dir):

        path = os.path.join(temp_dir, file)
        try:
            if not os.path.isfile(path):
                continue

            # There is an opportunity here to create a new
            # CSAR from "fixed" single YAML files (eg. TOSCA v1.3)
            handle_yaml(path, parsed_params)
        except Exception as e:
            errors.add(f"[{file}] {e}")

    if temp_dir:
        shutil.rmtree(temp_dir)

    return errors
