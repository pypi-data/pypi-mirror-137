DESCRIBE_FUNCTIONS = ("describe", "get", "search", "list")

DELETE_FUNCTIONS = (
    "delete",
    "disassociate",
    "reject",
    "deallocate",
    "unassign",
    "deregister",
    "deprovision",
    "revoke",
    "release",
    "terminate",
    "cancel",
    "disable",
)

CREATE_FUNCTIONS = (
    "create",
    "associate",
    "accept",
    "allocate",
    "assign",
    "register",
    "provision",
    "authorize",
    "run",
    "enable",
    "upload",
    "put",
    "publish",
)

NAME_PARAMETER = {
    "default": None,
    "doc": "A name, ID to identify the resource",
    "param_type": "Text",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}


PRESENT_REQUEST_FORMAT = r"""
    result = dict(comment="", old_state=None, new_state=None, name=name, result=True)
    {{ function.hardcoded.resource_function_call }}
    before = {{ function.hardcoded.describe_function_call }}
    if ctx.get("test", False):
        if before:
            result["comment"] = f"Would update aws.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource }} {name}"
            result["result"] = True
        else:
            result["comment"] = f"Would create aws.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource }} {name}"
            result["result"] = True
        return result

    if before:
        result["comment"] = f"'{name}' already exists"
        # TODO perform day-2 modifications as needed here
    else:
        try:
            ret = await {{ function.hardcoded.create_function }}(
                ctx,
                {{ "ClientToken=name," if function.hardcoded.has_client_token }}
                **{{ parameter.mapping.kwargs|default({}) }}
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = f"Created '{name}'"
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] = f"{e.__class__.__name__}: {e}"
            result["result"] = False

    {{ function.hardcoded.waiter_call }}
    # TODO perform other modifications as needed here
    ...

    try:
        after = {{ function.hardcoded.describe_function_call }}
        result["new_state"] = after
    except Exception as e:
        result["comment"] = str(e)
        result["result"] = False
    return result
"""

ABSENT_REQUEST_FORMAT = r"""
    result = dict(comment="", old_state=None, new_state=None, name=name, result=True)
    {{ function.hardcoded.resource_function_call }}
    before = {{ function.hardcoded.describe_function_call }}

    if not before:
        result["comment"] = f"'{name}' already absent"
    elif ctx.get("test", False):
        result["comment"] = f"Would delete aws.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource }} {name}"
        return result
    else:
        result["old_state"] = before
        try:
            ret = await {{ function.hardcoded.delete_function }}(
                ctx,
                {{ "ClientToken=name," if function.hardcoded.has_client_token }}
                **{{ parameter.mapping.kwargs|default({}) }}
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
            result["comment"] = f"Deleted '{name}'"
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] = f"{e.__class__.__name__}: {e}"

    {{ function.hardcoded.waiter_call }}

    after = {{ function.hardcoded.describe_function_call }}
    result["changes"] = differ.deep_diff(before, after)
    return result
"""

DESCRIBE_REQUEST_FORMAT = r"""
    result = {}
    ret = await {{ function.hardcoded.list_function}}(ctx)

    if not ret["status"]:
        hub.log.debug(f"Could not describe {{ function.hardcoded.resource }} {ret['comment']}")
        return {}

    for {{ function.hardcoded.resource }} in ret["ret"]["{{ function.hardcoded.list_item }}"]:
        # Including fields to match the 'present' function parameters
        # TODO convert the dictionary values from string to object by removing the quotes.
        # TODO From 'resource[param]' to resource[param]
        new_{{ function.hardcoded.resource }} = {{ function.hardcoded.present_params }}
        result[{{ function.hardcoded.resource }}["{{ function.hardcoded.resource_id }}"]] = {"{{ function.ref }}.present": new_{{ function.hardcoded.resource }}}

    return result
"""
