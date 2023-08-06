"""
Class object for Cpu
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from typing import List

from .base import BridgeBase
from .hardware_sensor import HardwareSensor


class Cache(BridgeBase):
    @property
    def l1d(self) -> int | None:
        return self.attributes.get("l1d")

    @property
    def l1i(self) -> int | None:
        return self.attributes.get("l1i")

    @property
    def l2(self) -> int | None:
        return self.attributes.get("l2")

    @property
    def l3(self) -> int | None:
        return self.attributes.get("l3")


class CpuCache(BridgeBase):
    @property
    def l1d(self) -> int | None:
        return self.attributes.get("l1d")

    @property
    def l1i(self) -> int | None:
        return self.attributes.get("l1i")

    @property
    def l2(self) -> int | None:
        return self.attributes.get("l2")

    @property
    def l3(self) -> int | None:
        return self.attributes.get("l3")


class CpuInner(BridgeBase):
    @property
    def manufacturer(self) -> str | None:
        return self.attributes.get("manufacturer")

    @property
    def brand(self) -> str | None:
        return self.attributes.get("brand")

    @property
    def vendor(self) -> str | None:
        return self.attributes.get("vendor")

    @property
    def family(self) -> str | None:
        return self.attributes.get("family")

    @property
    def model(self) -> str | None:
        return self.attributes.get("model")

    @property
    def stepping(self) -> str | None:
        return self.attributes.get("stepping")

    @property
    def revision(self) -> str | None:
        return self.attributes.get("revision")

    @property
    def voltage(self) -> str | None:
        return self.attributes.get("voltage")

    @property
    def speed(self) -> float | None:
        return self.attributes.get("speed")

    @property
    def speedMin(self) -> float | None:
        return self.attributes.get("speedMin")

    @property
    def speedMax(self) -> float | None:
        return self.attributes.get("speedMax")

    @property
    def governor(self) -> str | None:
        return self.attributes.get("governor")

    @property
    def cores(self) -> int | None:
        return self.attributes.get("cores")

    @property
    def physicalCores(self) -> int | None:
        return self.attributes.get("physicalCores")

    @property
    def processors(self) -> int | None:
        return self.attributes.get("processors")

    @property
    def socket(self) -> str | None:
        return self.attributes.get("socket")

    @property
    def flags(self) -> str | None:
        return self.attributes.get("flags")

    @property
    def virtualization(self) -> bool | None:
        return self.attributes.get("virtualization")

    @property
    def cache(self) -> CpuCache | None:
        return CpuCache(self.attributes.get("cache"))


class CurrentSpeed(BridgeBase):
    @property
    def min(self) -> float | None:
        return self.attributes.get("min")

    @property
    def max(self) -> float | None:
        return self.attributes.get("max")

    @property
    def avg(self) -> float | None:
        return self.attributes.get("avg")

    @property
    def cores(self) -> List[float] | None:
        return self.attributes.get("cores")


class Temperature(BridgeBase):
    @property
    def main(self) -> float | int | None:
        return self.attributes.get("main")

    @property
    def cores(self) -> List[float | int] | None:
        return self.attributes.get("cores")

    @property
    def max(self) -> float | int | None:
        return self.attributes.get("max")

    @property
    def socket(self) -> List[float | int] | None:
        return self.attributes.get("socket")

    @property
    def chipset(self) -> float | int | None:
        return self.attributes.get("chipset")


class Cpu(BridgeBase):
    @property
    def cache(self) -> Cache | None:
        return Cache(self.attributes.get("cache"))

    @property
    def cpu(self) -> CpuInner | None:
        return CpuInner(self.attributes.get("cpu"))

    @property
    def currentSpeed(self) -> CurrentSpeed | None:
        return CurrentSpeed(self.attributes.get("currentSpeed"))

    @property
    def temperature(self) -> Temperature | None:
        return Temperature(self.attributes.get("temperature"))

    @property
    def hardware_sensors(self) -> List[HardwareSensor] | None:
        return [HardwareSensor(x for x in self.attributes.get("hardwareSensors", []))]
