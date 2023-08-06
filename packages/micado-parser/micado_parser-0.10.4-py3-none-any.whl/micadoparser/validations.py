"""
MiCADO Submission Engine TOSCA Validator
-----------------------------------------

Validate ToscaTemplate objects to ensure syntactic and semantic compatibility
with custom defined and TOSCA normative types.

Further validates a ToscaTemplate which has already passed validation steps
set out by the OpenStack ToscaParser. Currently validation checks exist for
repositories and the requirements and relationships of custom defined types.
"""
from toscaparser.tosca_template import ToscaTemplate

from micadoparser.utils import utils
from micadoparser.exceptions import ValidationError


def validate_toscatemplate(tpl):
    """Validate TOSCA Template

    Checks to see if the provided template was correctly parsed into
    a TOSCA Template object. Raises TypeError if not.

    """
    if not isinstance(tpl, ToscaTemplate):
        raise ValidationError("[TPL] Not a valid TOSCA Template")
    return {}


def validate_topologytemplate(tpl):
    """Ensure Topology Template

    Checks to see if the provided ADT contains a topology_template.
    Raises TypeError if not.

    """
    if not hasattr(tpl, "nodetemplates"):
        raise ValidationError("[TPL] Missing node_templates")
    return {}


def validate_csar(tpl):
    """"""


def validate_repositories(node, tpl):
    """Validate repository names

    Checks to see if repositories have been defined at the top level, and if
    nodes reference those repositories correctly. Returns errors if not.

    """
    repository_names = [repository.name for repository in tpl.repositories]

    repositories = utils.key_search("repository", node.entity_tpl)
    return {
        "[NODE: {}] Repository <{}> not defined!".format(node.name, repo)
        for repo in repositories
        if repo not in repository_names
    }


def validate_requirements(node, tpl):
    """Validate requirements and their syntax

    Checks that requirements in custom_types and in node definitions are
    defined as one-item lists and that node definition requirements correctly
    reference requirements defined in custom_types. Returns errors if not.

    """
    if not utils.is_custom(node, tpl):
        return {}
    type_reqs = node.type_definition.requirements
    node_reqs = node.requirements

    type_req_names = utils.get_requirement_names(type_reqs)
    node_req_names = utils.get_requirement_names(node_reqs)

    msg = "Too many requirements per list item!"

    if len(type_reqs) != len(type_req_names):
        return {"[CUSTOM TYPE: {}] {}".format(node.type, msg)}

    elif len(node_reqs) != len(node_req_names):
        return {"[NODE: {}] {}".format(node.name, msg)}

    return {
        "[NODE: {}] Requirement <{}> not defined!".format(node.name, req)
        for req in node_req_names
        if req not in type_req_names
    }


def validate_relationships(node, tpl):
    """Validate relationships

    Checks that relationships used in node definitions correctly reference
    relationships defined in TOSCA normative or custom types. Returns errors
    if not.

    """
    if not utils.is_custom(node, tpl):
        return {}

    type_reqs = node.type_definition.requirements
    node_reqs = node.requirements
    errors = set()

    for node_req in node_reqs:
        relationships = utils.key_search(["relationship", "type"], node_req)
        supported_relationships = [
            utils.key_search(["relationship", "type"], type_req)
            for type_req in type_reqs
        ]

        errors.update(
            {
                "[NODE: {}] "
                "Relationship <{}> not supported!".format(node.name, relationship)
                for relationship in relationships
                if relationship not in str(supported_relationships)
            }
        )

    return errors


def validate_relationship_properties(node, tpl):
    """Validate relationship properties

    Checks that relationships defined properties required by their definition
    in TOSCA normative or custom types. Returns errors if not.

    """
    if not utils.is_custom(node, tpl):
        return {}

    errors = set()
    for req, prop, relation in utils.get_required_properties(node):
        if not utils.has_property(req, prop, relation):
            errors.update(
                {
                    "[NODE: {}] Relationship <{}> "
                    "missing property <{}>".format(node.name, relation, prop)
                }
            )
    return errors
