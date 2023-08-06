"""
Class object for SettingsPutResponse
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from ..base import BridgeBase


class SettingsPutPayload(BridgeBase):
    @property
    def value(self) -> bool | int | float | str | None:
        return self.attributes.get("value")
