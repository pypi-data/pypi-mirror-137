"""
Class object for Audio
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from typing import List
from ..base import BridgeBase


class AudioSettings(BridgeBase):
    @property
    def muted(self) -> bool | None:
        return self.attributes.get("muted", False)

    @property
    def volume(self) -> int | None:
        return self.attributes.get("volume", -1)


class AudioDevice(BridgeBase):
    @property
    def id(self) -> str | None:
        return self.attributes.get("id")

    @property
    def name(self) -> str | None:
        return self.attributes.get("name")

    @property
    def manufacturer(self) -> str | None:
        return self.attributes.get("manufacturer")

    @property
    def revision(self) -> str | None:
        return self.attributes.get("revision")

    @property
    def driver(self) -> str | None:
        return self.attributes.get("driver")

    @property
    def default(self) -> str | None:
        return self.attributes.get("default")

    @property
    def channel(self) -> str | None:
        return self.attributes.get("channel")

    @property
    def type(self) -> str | None:
        return self.attributes.get("type")

    @property
    def p_in(self) -> str | None:
        return self.attributes.get("in")

    @property
    def out(self) -> str | None:
        return self.attributes.get("out")

    @property
    def status(self) -> str | None:
        return self.attributes.get("status")


class Audio(BridgeBase):
    @property
    def current(self) -> AudioSettings | None:
        return self.attributes.get("current")

    @property
    def devices(self) -> List[AudioDevice] | None:
        return self.attributes.get("devices")
