"""
Class object for Bluetooth
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from .base import BridgeBase


class Bluetooth(BridgeBase):
    @property
    def device(self) -> str | None:
        return self.attributes.get("device")

    @property
    def name(self) -> str | None:
        return self.attributes.get("name")

    @property
    def manufacturer(self) -> str | None:
        return self.attributes.get("manufacturer")

    @property
    def macDevice(self) -> str | None:
        return self.attributes.get("macDevice")

    @property
    def macHost(self) -> str | None:
        return self.attributes.get("macHost")

    @property
    def batteryPercent(self) -> str | None:
        return self.attributes.get("batteryPercent")

    @property
    def type(self) -> str | None:
        return self.attributes.get("type")

    @property
    def connected(self) -> str | None:
        return self.attributes.get("connected")
