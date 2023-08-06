"""
MiCADO Submission Engine Utilities
---------------------------------------
Various utilities for the MiCADO Parser which did not fit elsewhere
"""


def resolve_get_functions(
    dict_to_search, key_to_find, test_result_fn, resolve_result_fn, *args
):
    """Recursively update a dict with TOSCA 'get' functions

    Args:
        dict_to_search (dict): Dictionary to iterate through
        key_to_find (str): 'get' function to search for (eg 'get_input')
        test_result_fn (func): Function to test the result
        resolve_result_fn (func): Function to resolve the result
        args (*): Extra args to pass to resolve_result_fn

    Returns:
        None: Modifies the dictionary in place
    """
    for key, value in dict_to_search.items():
        if key == key_to_find:
            return value

        elif isinstance(value, dict):
            result = resolve_get_functions(
                value, key_to_find, test_result_fn, resolve_result_fn, *args
            )
            if test_result_fn(result):
                dict_to_search[key] = resolve_result_fn(result, *args)

        elif isinstance(value, list):
            for index, item in enumerate(value):
                if not isinstance(item, dict):
                    continue
                result = resolve_get_functions(
                    item, key_to_find, test_result_fn, resolve_result_fn, *args
                )
                if test_result_fn(result):
                    dict_to_search[key][index] = resolve_result_fn(result, *args)


def is_custom(node, tpl):
    """Determine if node is of a custom type"""
    custom_types = tuple(tpl.topology_template.custom_defs.keys())
    return True if node.type in custom_types else False


def has_property(requirements, prop, rel_type):
    """Check if a requirement has the correct properties and type"""
    for requirement_dict in requirements:
        for requirement in requirement_dict.values():
            if isinstance(requirement, str):
                return True
            relation = requirement.get("relationship")
            if isinstance(relation, dict) and rel_type in relation.get("type"):
                if prop in str(requirement_dict):
                    return True
    return False


def get_requirement_names(req_dict):
    """Get requirement names"""
    return [
        requirement
        for requirements in [list(req.keys()) for req in req_dict]
        for requirement in requirements
    ]


def get_required_properties(node):
    """Generate required properties"""
    for relation in node.related.values():
        for prop, prop_obj in relation.get_properties_def().items():
            if prop_obj.required:
                yield (node.requirements, prop, relation.type)


def key_search(query, node):
    """Search through the raw data of a node for a value given a key"""

    def flatten_pairs(nest):
        """Recursively crawl through a nested dictionary"""
        for key, val in nest.items():
            if isinstance(val, dict):
                yield from flatten_pairs(val)
            elif isinstance(val, list):
                for listitem in val:
                    if isinstance(listitem, dict):
                        yield from flatten_pairs(listitem)
            else:
                yield key, val

    return [val for key, val in flatten_pairs(node) if key in query]


def is_csar(file):
    """Check if file is a CSAR multi-file ADT"""
    return file.casefold().endswith("csar".casefold())
