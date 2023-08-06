"""
Class object for HardwareSensor
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from .base import BridgeBase


class HardwareSensor(BridgeBase):
    @property
    def id(self) -> str | None:
        self.attributes.get("id")

    @property
    def name(self) -> str | None:
        self.attributes.get("name")

    @property
    def type(self) -> str | None:
        self.attributes.get("type")

    @property
    def value(self) -> bool | float | int | str | None:
        self.attributes.get("value")
