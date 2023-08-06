"""
Class object for Display
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations
from typing import List

from ..base import BridgeBase


class Display(BridgeBase):
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

    @property
    def currentRefreshRate(self) -> int | None:
        return self.attributes.get("currentRefreshRate")


class DisplayBase(BridgeBase):
    @property
    def displays(self) -> List[Display]:
        return [Display(display) for display in self.attributes.get("displays")]
