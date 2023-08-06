"""
Class object for Settings
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from ..base import BridgeBase


class Settings(BridgeBase):
    @property
    def section(self) -> str | None:
        return self.attributes.get("section")

    @property
    def key(self) -> str | None:
        return self.attributes.get("key")

    @property
    def name(self) -> str | None:
        return self.attributes.get("name")

    @property
    def description(self) -> str | None:
        return self.attributes.get("description")

    @property
    def defaultValue(self) -> str | None:
        return self.attributes.get("defaultValue")

    @property
    def value(self) -> str | float | int | bool | None:
        return self.attributes.get("value")

    @property
    def icon(self) -> str | None:
        return self.attributes.get("icon")

    @property
    def requiresServerRestart(self) -> bool | None:
        return self.attributes.get("requiresServerRestart")
