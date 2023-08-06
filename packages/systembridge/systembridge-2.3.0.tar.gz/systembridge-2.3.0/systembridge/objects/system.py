"""
Class object for System
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from .base import BridgeBase


class Baseboard(BridgeBase):
    @property
    def manufacturer(self) -> str | None:
        return self.attributes.get("manufacturer")

    @property
    def model(self) -> str | None:
        return self.attributes.get("model")

    @property
    def version(self) -> str | None:
        return self.attributes.get("version")

    @property
    def serial(self) -> str | None:
        return self.attributes.get("serial")

    @property
    def assetTag(self) -> str | None:
        return self.attributes.get("assetTag")

    @property
    def memMax(self) -> int | None:
        return self.attributes.get("memMax")

    @property
    def memSlots(self) -> int | None:
        return self.attributes.get("memSlots")


class Bios(BridgeBase):
    @property
    def vendor(self) -> str | None:
        return self.attributes.get("vendor")

    @property
    def version(self) -> str | None:
        return self.attributes.get("version")

    @property
    def releaseDate(self) -> str | None:
        return self.attributes.get("releaseDate")

    @property
    def revision(self) -> str | None:
        return self.attributes.get("revision")


class Chassis(BridgeBase):
    @property
    def manufacturer(self) -> str | None:
        return self.attributes.get("manufacturer")

    @property
    def model(self) -> str | None:
        return self.attributes.get("model")

    @property
    def type(self) -> str | None:
        return self.attributes.get("type")

    @property
    def version(self) -> str | None:
        return self.attributes.get("version")

    @property
    def serial(self) -> str | None:
        return self.attributes.get("serial")

    @property
    def assetTag(self) -> str | None:
        return self.attributes.get("assetTag")

    @property
    def sku(self) -> str | None:
        return self.attributes.get("sku")


class SystemInner(BridgeBase):
    @property
    def manufacturer(self) -> str | None:
        return self.attributes.get("manufacturer")

    @property
    def model(self) -> str | None:
        return self.attributes.get("model")

    @property
    def version(self) -> str | None:
        return self.attributes.get("version")

    @property
    def serial(self) -> str | None:
        return self.attributes.get("serial")

    @property
    def uuid(self) -> str | None:
        return self.attributes.get("uuid")

    @property
    def sku(self) -> str | None:
        return self.attributes.get("sku")

    @property
    def virtual(self) -> bool | None:
        return self.attributes.get("virtual")


class Uuid(BridgeBase):
    @property
    def os(self) -> str | None:
        return self.attributes.get("os")

    @property
    def hardware(self) -> str | None:
        return self.attributes.get("hardware")

    @property
    def macs(self) -> str | None:
        return self.attributes.get("macs")


class System(BridgeBase):
    @property
    def baseboard(self) -> str | None:
        return Baseboard(self.attributes.get("baseboard", {}))

    @property
    def bios(self) -> str | None:
        return Bios(self.attributes.get("bios", {}))

    @property
    def chassis(self) -> str | None:
        return Chassis(self.attributes.get("chassis", {}))

    @property
    def system(self) -> str | None:
        return SystemInner(self.attributes.get("system", {}))

    @property
    def uuid(self) -> str | None:
        return Uuid(self.attributes.get("uuid", {}))
