from typing import Any
from typing import Dict
from typing import List


async def update_instance_profile_tags(
    hub,
    ctx,
    instance_profile_name: str,
    old_tags: List[Dict[str, Any]],
    new_tags: List[Dict[str, Any]],
):
    """
    Update tags of AWS IAM Instance Profile

    TODO - this method might fail with localstack but is successful with a real AWS account

    Args:
        hub: The redistributed pop central hub.
        ctx: A dict with the keys/values for the execution of the Idem run located in
        `hub.idem.RUNS[ctx['run_name']]`.
        instance_profile_name: AWS IAM instance profile name
        old_tags: list of old tags
        new_tags: list of new tags

    Returns:
        {"result": True|False, "comment": "A message", "ret": None}
    """
    result = dict(comment="", result=True, ret=None)

    tags_to_add = list()
    old_tags_map = {tag.get("Key"): tag for tag in old_tags}
    for tag in new_tags:
        if tag.get("Key") in old_tags_map:
            del old_tags_map[tag.get("Key")]
        else:
            tags_to_add.append(tag)
    tags_to_remove = [tag.get("Key") for tag in old_tags_map.values()]
    if tags_to_add:
        add_ret = await hub.exec.boto3.client.iam.tag_instance_profile(
            ctx, InstanceProfileName=instance_profile_name, Tags=tags_to_add
        )
        if not add_ret["result"]:
            result["comment"] = add_ret["comment"]
            result["result"] = False
            return result
    if tags_to_remove:
        delete_ret = await hub.exec.boto3.client.iam.untag_instance_profile(
            ctx, InstanceProfileName=instance_profile_name, TagKeys=tags_to_remove
        )
        if not delete_ret["result"]:
            result["comment"] = delete_ret["comment"]
            result["result"] = False
            return result
    result[
        "comment"
    ] = f"Update tags on instance-profile: Add [{tags_to_add}] Remove [{tags_to_remove}]"
    return result
