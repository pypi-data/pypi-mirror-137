from typing import Any
from typing import Dict
from typing import List


async def update_policy(
    hub, ctx, policy_arn: str, policy_version_id: str, new_policy_document: str
) -> Dict[str, Any]:
    """
    Update the policy document of an existing managed policy.

    Args:
        hub: The redistributed pop central hub.
        ctx: A dict with the keys/values for the execution of the Idem run located in
        `hub.idem.RUNS[ctx['run_name']]`.
        policy_arn: The Amazon Resource Name (ARN) of the managed policy that you want information about.
        policy_version_id: Identifies the policy version to retrieve. This parameter allows (through its regex pattern)
         a string of characters that consists of the lowercase letter 'v' followed by one or two digits, and optionally
          followed by a period '.' and a string of letters and digits.
        new_policy_document: The JSON policy document that you want to use as the content for the new policy.

    Returns:
        {"result": True|False, "comment": "A message", "ret": None}
    """
    result = dict(comment="", result=True, ret=None)
    if new_policy_document is None:
        result["comment"] = f"Skip aws.iam.policy update. New policy document is None"
        return result
    get_ret = await hub.exec.boto3.client.iam.get_policy_version(
        ctx=ctx, PolicyArn=policy_arn, VersionId=policy_version_id
    )
    if not get_ret["result"]:
        result["result"] = False
        result["comment"] = get_ret["comment"]
        return result
    old_policy = get_ret["ret"]
    if old_policy.get("PolicyVersion").get("Document") == new_policy_document:
        result["comment"] = "No need to update aws.iam.policy policy document"
        return result
    try:
        # Update the policy document by creating a new policy document, set it to default, and then delete the old
        # policy document
        create_ret = await hub.exec.boto3.client.iam.create_policy_version(
            ctx=ctx,
            PolicyArn=policy_arn,
            PolicyDocument=new_policy_document,
            SetAsDefault=True,
        )
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] = create_ret["comment"]
            return result
        delete_ret = await hub.exec.boto3.client.iam.delete_policy_version(
            ctx=ctx, PolicyArn=policy_arn, VersionId=policy_version_id
        )
        if not delete_ret["result"]:
            hub.log.warning(
                f"hub.exec.aws.iam.policy.update_policy failed to delete policy document with version"
                f" {policy_version_id} . Manual cleanup may be needed."
            )
            result["comment"] = (
                f"hub.exec.aws.iam.policy.update_policy failed to delete policy document with version"
                f" {policy_version_id} . Manual cleanup may be needed."
            )
        else:
            result["comment"] = (
                f"hub.exec.aws.iam.policy.update_policy updated policy document to version"
                f" {create_ret['ret'].get('PolicyVersion').get('VersionId')}"
            )
    except Exception as e:
        result["comment"] = str(e)
        result["result"] = False
    return result


async def update_policy_tags(
    hub,
    ctx,
    police_arn: str,
    old_tags: List[Dict[str, Any]],
    new_tags: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Update tags of AWS IAM Policy

    Args:
        hub: The redistributed pop central hub.
        ctx: A dict with the keys/values for the execution of the Idem run located in
        `hub.idem.RUNS[ctx['run_name']]`.
        police_arn: The ARN of the IAM customer managed policy to which you want to add tags.
         This parameter allows (through its regex pattern) a string of characters consisting of upper and lowercase
          alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        old_tags: list of old tags
        new_tags: list of new tags

    Returns:
        {"result": True|False, "comment": "A message", "ret": None}
    """
    tags_to_add = list()
    if old_tags is None:
        old_tags = list()
    old_tags_map = {tag.get("Key"): tag for tag in old_tags}
    for tag in new_tags:
        if tag.get("Key") in old_tags_map:
            del old_tags_map[tag.get("Key")]
        else:
            tags_to_add.append(tag)
    tags_to_remove = [tag.get("Key") for tag in old_tags_map.values()]
    result = dict(comment="", result=True, ret=None)
    if tags_to_add:
        add_ret = await hub.exec.boto3.client.iam.tag_policy(
            ctx, PolicyArn=police_arn, Tags=tags_to_add
        )
        if not add_ret["result"]:
            result["comment"] = add_ret["comment"]
            result["result"] = False
            return result
    if tags_to_remove:
        delete_ret = await hub.exec.boto3.client.iam.untag_policy(
            ctx, PolicyArn=police_arn, TagKeys=tags_to_remove
        )
        if not delete_ret["result"]:
            result["comment"] = delete_ret["comment"]
            result["result"] = False
            return result
    result[
        "comment"
    ] = f"Update policy with arn {police_arn} tags: Add [{tags_to_add}] Remove [{tags_to_remove}]"
    return result
