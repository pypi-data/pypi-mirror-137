"""
Class object for Graphics
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from typing import List

from .base import BridgeBase
from .hardware_sensor import HardwareSensor


class Controllers(BridgeBase):
    @property
    def vendor(self) -> str | None:
        return self.attributes.get("vendor")

    @property
    def model(self) -> str | None:
        return self.attributes.get("model")

    @property
    def bus(self) -> str | None:
        return self.attributes.get("bus")

    @property
    def vram(self) -> int | None:
        return self.attributes.get("vram")

    @property
    def vramDynamic(self) -> bool | None:
        return self.attributes.get("vramDynamic")

    @property
    def subDeviceId(self) -> str | None:
        return self.attributes.get("subDeviceId")

    @property
    def driverVersion(self) -> str | None:
        return self.attributes.get("driverVersion")

    @property
    def name(self) -> str | None:
        return self.attributes.get("name")

    @property
    def pciBus(self) -> str | None:
        return self.attributes.get("pciBus")

    @property
    def fanSpeed(self) -> int | None:
        return self.attributes.get("fanSpeed")

    @property
    def memoryTotal(self) -> int | None:
        return self.attributes.get("memoryTotal")

    @property
    def memoryUsed(self) -> int | None:
        return self.attributes.get("memoryUsed")

    @property
    def memoryFree(self) -> int | None:
        return self.attributes.get("memoryFree")

    @property
    def utilizationGpu(self) -> int | None:
        return self.attributes.get("utilizationGpu")

    @property
    def utilizationMemory(self) -> int | None:
        return self.attributes.get("utilizationMemory")

    @property
    def temperatureGpu(self) -> int | None:
        return self.attributes.get("temperatureGpu")

    @property
    def powerDraw(self) -> float | None:
        return self.attributes.get("powerDraw")

    @property
    def powerLimit(self) -> float | None:
        return self.attributes.get("powerLimit")

    @property
    def clockCore(self) -> int | None:
        return self.attributes.get("clockCore")

    @property
    def clockMemory(self) -> int | None:
        return self.attributes.get("clockMemory")


class Displays(BridgeBase):
    @property
    def vendor(self) -> str | None:
        return self.attributes.get("vendor")

    @property
    def model(self) -> str | None:
        return self.attributes.get("model")

    @property
    def deviceName(self) -> str | None:
        return self.attributes.get("deviceName")

    @property
    def main(self) -> bool | None:
        return self.attributes.get("main")

    @property
    def builtin(self) -> bool | None:
        return self.attributes.get("builtin")

    @property
    def connection(self) -> str | None:
        return self.attributes.get("connection")

    @property
    def resolutionX(self) -> int | None:
        return self.attributes.get("resolutionX")

    @property
    def resolutionY(self) -> int | None:
        return self.attributes.get("resolutionY")

    @property
    def sizeX(self) -> int | None:
        return self.attributes.get("sizeX")

    @property
    def sizeY(self) -> int | None:
        return self.attributes.get("sizeY")

    @property
    def pixelDepth(self) -> str | None:
        return self.attributes.get("pixelDepth")

    @property
    def currentResX(self) -> int | None:
        return self.attributes.get("currentResX")

    @property
    def currentResY(self) -> int | None:
        return self.attributes.get("currentResY")

    @property
    def positionX(self) -> int | None:
        return self.attributes.get("positionX")

    @property
    def positionY(self) -> int | None:
        return self.attributes.get("positionY")


class Graphics(BridgeBase):
    @property
    def controllers(self) -> List[Controllers] | None:
        return [Controllers(x) for x in self.attributes.get("controllers", [])]

    @property
    def displays(self) -> List[Displays] | None:
        return [Displays(x) for x in self.attributes.get("displays", [])]

    @property
    def hardware_sensors(self) -> List[HardwareSensor] | None:
        return [HardwareSensor(x for x in self.attributes.get("hardwareSensors", []))]
