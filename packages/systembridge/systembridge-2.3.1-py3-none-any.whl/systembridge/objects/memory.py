"""
Class object for Memory
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations
from typing import List

from .base import BridgeBase


class Layout(BridgeBase):
    @property
    def size(self) -> int | None:
        return self.attributes.get("size")

    @property
    def bank(self) -> str | None:
        return self.attributes.get("bank")

    @property
    def type(self) -> str | None:
        return self.attributes.get("type")

    @property
    def ecc(self) -> bool | None:
        return self.attributes.get("ecc")

    @property
    def clockSpeed(self) -> float | int | None:
        return self.attributes.get("clockSpeed")

    @property
    def formFactor(self) -> str | None:
        return self.attributes.get("formFactor")

    @property
    def manufacturer(self) -> str | None:
        return self.attributes.get("manufacturer")

    @property
    def partNum(self) -> str | None:
        return self.attributes.get("partNum")

    @property
    def serialNum(self) -> str | None:
        return self.attributes.get("serialNum")

    @property
    def voltageConfigured(self) -> float | None:
        return self.attributes.get("voltageConfigured")

    @property
    def voltageMin(self) -> float | None:
        return self.attributes.get("voltageMin")

    @property
    def voltageMax(self) -> float | None:
        return self.attributes.get("voltageMax")


class Memory(BridgeBase):
    @property
    def total(self) -> int | None:
        return self.attributes.get("total")

    @property
    def free(self) -> int | None:
        return self.attributes.get("free")

    @property
    def used(self) -> int | None:
        return self.attributes.get("used")

    @property
    def active(self) -> int | None:
        return self.attributes.get("active")

    @property
    def available(self) -> int | None:
        return self.attributes.get("available")

    @property
    def buffers(self) -> int | None:
        return self.attributes.get("buffers")

    @property
    def cached(self) -> int | None:
        return self.attributes.get("cached")

    @property
    def slab(self) -> int | None:
        return self.attributes.get("slab")

    @property
    def buffcache(self) -> int | None:
        return self.attributes.get("buffcache")

    @property
    def swaptotal(self) -> int | None:
        return self.attributes.get("swaptotal")

    @property
    def swapused(self) -> int | None:
        return self.attributes.get("swapused")

    @property
    def swapfree(self) -> int | None:
        return self.attributes.get("swapfree")

    @property
    def layout(self) -> List[Layout] | None:
        return [Layout(x) for x in self.attributes.get("layout", [])]
