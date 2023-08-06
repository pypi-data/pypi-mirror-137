"""
Class object for KeyboardPayload
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from typing import List, Optional
from ..base import BridgeBase


class KeyboardPayload(BridgeBase):
    @property
    def key(self) -> str | None:
        return self.attributes.get("key")

    @property
    def modifiers(self) -> List[str] | None:
        return self.attributes.get("modifiers")

    @property
    def text(self) -> str | None:
        return self.attributes.get("text")
