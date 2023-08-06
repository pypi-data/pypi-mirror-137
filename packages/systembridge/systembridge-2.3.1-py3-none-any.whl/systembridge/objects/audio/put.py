"""
Class object for AudioPutPayload and AudioPutResponse
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from . import Audio
from ..base import BridgeBase


class AudioPutPayload(BridgeBase):
    @property
    def value(self) -> bool | float | None:
        return self.attributes.get("value", True)


class AudioPutResponse(Audio):
    @property
    def successful(self) -> bool | None:
        return self.attributes.get("successful", False)
