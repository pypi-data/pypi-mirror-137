"""
Class object for CommandPayload
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from typing import List

from ..base import BridgeBase


class CommandPayload(BridgeBase):
    @property
    def command(self) -> str:
        return self.attributes.get("command")

    @property
    def arguments(self) -> List[str]:
        return self.attributes.get("arguments", [])

    @property
    def wait(self) -> bool:
        return self.attributes.get("wait", True)
