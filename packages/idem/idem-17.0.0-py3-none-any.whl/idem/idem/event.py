from typing import Any
from typing import Dict


async def put(
    hub,
    body: Any,
    profile: str = "default",
    routing_key: str = None,
    tags: Dict[str, Any] = None,
):
    if routing_key is None:
        routing_key = hub.OPT.idem.run_name
    if tags is None:
        tags = {}

    await hub.evbus.broker.put(
        routing_key=routing_key, profile=profile, body=dict(tags=tags, message=body)
    )


def put_nowait(
    hub,
    body: Any,
    profile: str = "default",
    routing_key: str = None,
    tags: Dict[str, Any] = None,
):
    if routing_key is None:
        routing_key = hub.OPT.idem.run_name
    if tags is None:
        tags = {}

    hub.evbus.broker.put_nowait(
        routing_key=routing_key, profile=profile, body=dict(tags=tags, message=body)
    )
