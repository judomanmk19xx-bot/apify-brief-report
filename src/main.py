"""Brief Report — Apify Actor.

Thin wrapper around the Mekong Trade Intelligence morning-brief service
(https://api.mekongtradeintel.com/brief/). The buyer pays on Apify via
pay-per-event; the Actor executes the brief through a dedicated channel
key (env MTI_CHANNEL_KEY, set as a secret by the Actor owner) and pushes
the finished brief as one dataset item.

Charge policy: the pay-per-event charge happens ONLY after the brief has
completed and its result has been pushed to the dataset. A failed brief
fails the run and is never charged.
"""

import asyncio
import os

import httpx
from apify import Actor

JOB_URL = "https://api.mekongtradeintel.com/brief/"
EVENT_NAME = "brief-report"
JOB_TIMEOUT_S = 600  # a full brief (news + trends + sentiment) can take minutes


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        topic = str(actor_input.get("topic") or "").strip()

        if not topic:
            await Actor.fail("Input 'topic' is required.")
            return

        channel_key = os.environ.get("MTI_CHANNEL_KEY", "").strip()
        if not channel_key:
            await Actor.fail("Actor is not configured (missing channel key).")
            return

        payload = {"topic": topic}

        Actor.log.info(f"Running brief for topic: {topic}")

        async with httpx.AsyncClient(timeout=JOB_TIMEOUT_S, trust_env=False) as client:
            resp = await client.post(
                JOB_URL,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "X-Channel-Key": channel_key,
                    "User-Agent": "ApifyActor-BriefReport/1.0",
                },
            )

        if resp.status_code != 200:
            await Actor.fail(
                f"Brief failed with HTTP {resp.status_code}: {resp.text[:300]}"
            )
            return

        result = resp.json()

        # One dataset item per brief: the full brief JSON.
        await Actor.push_data(result)
        Actor.log.info("Brief completed and pushed to dataset.")

        # Charge only after successful delivery.
        try:
            await Actor.charge(event_name=EVENT_NAME, count=1)
            Actor.log.info(f"Charged 1 x '{EVENT_NAME}' event.")
        except Exception as exc:  # billing must never mask a delivered result
            Actor.log.warning(f"Charge call failed (result already delivered): {exc}")


if __name__ == "__main__":
    asyncio.run(main())
