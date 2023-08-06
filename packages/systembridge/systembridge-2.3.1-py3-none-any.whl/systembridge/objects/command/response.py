"""
Class object for CommandResponse
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from .payload import CommandPayload


class CommandResponse(CommandPayload):
    @property
    def success(self) -> bool | None:
        return self.attributes.get("success")

    @property
    def message(self) -> str | None:
        return self.attributes.get("message")
