"""
Class object for Battery
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from .base import BridgeBase


class Battery(BridgeBase):
    @property
    def hasBattery(self) -> bool:
        return self.attributes.get("hasBattery")

    @property
    def cycleCount(self) -> int:
        return self.attributes.get("cycleCount")

    @property
    def isCharging(self) -> bool:
        return self.attributes.get("isCharging")

    @property
    def designedCapacity(self) -> float | None:
        return self.attributes.get("designedCapacity")

    @property
    def maxCapacity(self) -> float | None:
        return self.attributes.get("maxCapacity")

    @property
    def currentCapacity(self) -> float | None:
        return self.attributes.get("currentCapacity")

    @property
    def voltage(self) -> float | None:
        return self.attributes.get("voltage")

    @property
    def capacityUnit(self) -> str | None:
        return self.attributes.get("capacityUnit")

    @property
    def percent(self) -> float | None:
        return self.attributes.get("percent")

    @property
    def timeRemaining(self) -> str | float | None:
        return self.attributes.get("timeRemaining")

    @property
    def acConnected(self) -> bool | None:
        return self.attributes.get("acConnected")

    @property
    def type(self) -> str | None:
        return self.attributes.get("type")

    @property
    def model(self) -> str | None:
        return self.attributes.get("model")

    @property
    def manufacturer(self) -> str | None:
        return self.attributes.get("manufacturer")

    @property
    def serial(self) -> str | None:
        return self.attributes.get("serial")
