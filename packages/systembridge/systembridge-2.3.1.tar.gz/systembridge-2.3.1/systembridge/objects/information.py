"""
Class object for Information
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from .base import BridgeBase


class UpdatesVersion(BridgeBase):
    @property
    def current(self) -> str | None:
        return self.attributes.get("current")

    @property
    def new(self) -> str | None:
        return self.attributes.get("new")


class Updates(BridgeBase):
    @property
    def available(self) -> bool | None:
        return self.attributes.get("available", False)

    @property
    def newer(self) -> bool | None:
        return self.attributes.get("newer", False)

    @property
    def url(self) -> str | None:
        return self.attributes.get("url")

    @property
    def version(self) -> UpdatesVersion:
        return UpdatesVersion(self.attributes.get("version", {}))


class Information(BridgeBase):
    @property
    def address(self) -> str | None:
        return self.attributes.get("address")

    @property
    def apiPort(self) -> int | None:
        return self.attributes.get("apiPort", 9170)

    @property
    def fqdn(self) -> str | None:
        return self.attributes.get("fqdn")

    @property
    def host(self) -> str | None:
        return self.attributes.get("host")

    @property
    def ip(self) -> str | None:
        return self.attributes.get("ip")

    @property
    def mac(self) -> str | None:
        return self.attributes.get("mac")

    @property
    def updates(self) -> Updates:
        return Updates(self.attributes.get("updates"))

    @property
    def uuid(self) -> str | None:
        return self.attributes.get("uuid")

    @property
    def version(self) -> str | None:
        return self.attributes.get("version")

    @property
    def websocketAddress(self) -> str | None:
        return self.attributes.get("websocketAddress")

    @property
    def websocketPort(self) -> int | None:
        return self.attributes.get("websocketPort", 9172)
