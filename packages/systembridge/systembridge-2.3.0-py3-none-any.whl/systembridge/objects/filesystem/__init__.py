"""
Class object for Filesystem
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from typing import Any, Dict
from ..base import BridgeBase


class BlockDevices(BridgeBase):
    @property
    def name(self) -> str | None:
        return self.attributes.get("name")

    @property
    def identifier(self) -> str | None:
        return self.attributes.get("identifier")

    @property
    def type(self) -> str | None:
        return self.attributes.get("type")

    @property
    def fsType(self) -> str | None:
        return self.attributes.get("fsType")

    @property
    def mount(self) -> str | None:
        return self.attributes.get("mount")

    @property
    def size(self) -> str | None:
        return self.attributes.get("size")

    @property
    def physical(self) -> str | None:
        return self.attributes.get("physical")

    @property
    def uuid(self) -> str | None:
        return self.attributes.get("uuid")

    @property
    def label(self) -> str | None:
        return self.attributes.get("label")

    @property
    def model(self) -> str | None:
        return self.attributes.get("model")

    @property
    def serial(self) -> str | None:
        return self.attributes.get("serial")

    @property
    def removable(self) -> bool | None:
        return self.attributes.get("removable", False)

    @property
    def protocol(self) -> str | None:
        return self.attributes.get("protocol")


class DiskLayout(BridgeBase):
    @property
    def device(self) -> str | None:
        return self.attributes.get("device")

    @property
    def type(self) -> str | None:
        return self.attributes.get("type")

    @property
    def name(self) -> str | None:
        return self.attributes.get("name")

    @property
    def vendor(self) -> str | None:
        return self.attributes.get("vendor")

    @property
    def size(self) -> float | int | None:
        return self.attributes.get("size")

    @property
    def bytesPerSector(self) -> int | None:
        return self.attributes.get("bytesPerSector")

    @property
    def totalCylinders(self) -> int | None:
        return self.attributes.get("totalCylinders")

    @property
    def totalHeads(self) -> int | None:
        return self.attributes.get("totalHeads")

    @property
    def totalSectors(self) -> int | None:
        return self.attributes.get("totalSectors")

    @property
    def totalTracks(self) -> int | None:
        return self.attributes.get("totalTracks")

    @property
    def tracksPerCylinder(self) -> int | None:
        return self.attributes.get("tracksPerCylinder")

    @property
    def sectorsPerTrack(self) -> int | None:
        return self.attributes.get("sectorsPerTrack")

    @property
    def firmwareRevision(self) -> str | None:
        return self.attributes.get("firmwareRevision")

    @property
    def serialNum(self) -> str | None:
        return self.attributes.get("serialNum")

    @property
    def interfaceType(self) -> str | None:
        return self.attributes.get("interfaceType")

    @property
    def smartStatus(self) -> str | None:
        return self.attributes.get("smartStatus")

    @property
    def temperature(self) -> float | None:
        return self.attributes.get("temperature")


class FsSize(BridgeBase):
    @property
    def fs(self) -> str | None:
        return self.attributes.get("fs")

    @property
    def type(self) -> str | None:
        return self.attributes.get("type")

    @property
    def size(self) -> int | None:
        return self.attributes.get("size")

    @property
    def used(self) -> int | None:
        return self.attributes.get("used")

    @property
    def available(self) -> int | None:
        return self.attributes.get("available")

    @property
    def use(self) -> float | None:
        return self.attributes.get("use")

    @property
    def mount(self) -> str | None:
        return self.attributes.get("mount")


class Filesystem(BridgeBase):
    @property
    def blockDevices(self) -> Dict[str, BlockDevices] | None:
        return self.attributes.get("blockDevices")

    @property
    def diskLayout(self) -> Dict[str, DiskLayout] | None:
        return self.attributes.get("diskLayout")

    @property
    def disksIO(self) -> Dict[str, Any] | None:
        return self.attributes.get("disksIO")

    @property
    def fsSize(self) -> Dict[str, FsSize] | None:
        return self.attributes.get("fsSize")
