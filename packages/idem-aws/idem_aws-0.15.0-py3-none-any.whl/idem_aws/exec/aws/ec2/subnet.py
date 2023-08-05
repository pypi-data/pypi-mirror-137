from typing import Any
from typing import Dict


async def update_ipv6_cidr_blocks(
    hub,
    ctx,
    subnet_id: str,
    old_ipv6_cidr_block: Dict[str, Any],
    new_ipv6_cidr_block: Dict[str, Any],
):
    """
    Update associated ipv6 cidr block of a subnet. This function supports associating an ipv6 cidr block, or updating
     the existing(old) ipv6 cidr block to the new ipv6 cidr block. Disassociating an ipv6 cidr block is not supported,
     due to how an sls file works currently. If ipv6_cidr_block parameter is left as blank, Idem-aws will do no-op
     on the subnet's ipv6 cidr block. To disassociate an ipv6 cidr block, a user will have to delete the subnet and
     re-create it without the ipv6 cidr block.

    Args:
        hub:
        ctx:
        subnet_id: The AWS resource id of the existing subnet
        old_ipv6_cidr_block: The ipv6 cidr block on the existing vpc
        new_ipv6_cidr_block: The expected ipv6 cidr block on the existing vpc

    Returns:
        {"result": True|False, "comment": "A message", "ret": None}

    """
    result = dict(comment="", result=True, ret=None)
    ret = None
    if old_ipv6_cidr_block is None and new_ipv6_cidr_block:
        ret = await hub.exec.boto3.client.ec2.associate_subnet_cidr_block(
            ctx,
            SubnetId=subnet_id,
            Ipv6CidrBlock=new_ipv6_cidr_block.get("Ipv6CidrBlock"),
        )
        hub.log.info(
            f"Add subnet {subnet_id} ipv6 cidr block {new_ipv6_cidr_block.get('Ipv6CidrBlock')}"
        )
    elif old_ipv6_cidr_block and new_ipv6_cidr_block:
        if old_ipv6_cidr_block.get("Ipv6CidrBlock") != new_ipv6_cidr_block.get(
            "Ipv6CidrBlock"
        ):
            ret = await hub.exec.boto3.client.ec2.disassociate_subnet_cidr_block(
                ctx, AssociationId=old_ipv6_cidr_block.get("AssociationId")
            )
            if not ret.get("result"):
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
            ret = await hub.exec.boto3.client.ec2.associate_subnet_cidr_block(
                ctx,
                SubnetId=subnet_id,
                Ipv6CidrBlock=new_ipv6_cidr_block.get("Ipv6CidrBlock"),
            )
            if ret.get("result"):
                hub.log.info(
                    f"Update subnet {subnet_id} ipv6 cidr block from {old_ipv6_cidr_block.get('Ipv6CidrBlock')}"
                    f" to {new_ipv6_cidr_block.get('Ipv6CidrBlock')}"
                )
    if ret is not None:
        result["comment"] = ret["comment"]
        result["result"] = ret["result"]
    return result
