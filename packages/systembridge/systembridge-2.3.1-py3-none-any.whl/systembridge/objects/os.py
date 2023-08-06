"""
Class object for Os
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from typing import List
from .base import BridgeBase


class Users(BridgeBase):
    @property
    def user(self) -> str | None:
        return self.attributes.get("user")

    @property
    def tty(self) -> str | None:
        return self.attributes.get("tty")

    @property
    def date(self) -> str | None:
        return self.attributes.get("date")

    @property
    def time(self) -> str | None:
        return self.attributes.get("time")

    @property
    def ip(self) -> str | None:
        return self.attributes.get("ip")

    @property
    def command(self) -> str | None:
        return self.attributes.get("command")


class Os(BridgeBase):
    @property
    def platform(self) -> str | None:
        return self.attributes.get("platform")

    @property
    def distro(self) -> str | None:
        return self.attributes.get("distro")

    @property
    def release(self) -> str | None:
        return self.attributes.get("release")

    @property
    def codename(self) -> str | None:
        return self.attributes.get("codename")

    @property
    def kernel(self) -> str | None:
        return self.attributes.get("kernel")

    @property
    def arch(self) -> str | None:
        return self.attributes.get("arch")

    @property
    def hostname(self) -> str | None:
        return self.attributes.get("hostname")

    @property
    def fqdn(self) -> str | None:
        return self.attributes.get("fqdn")

    @property
    def codepage(self) -> str | None:
        return self.attributes.get("codepage")

    @property
    def logofile(self) -> str | None:
        return self.attributes.get("logofile")

    @property
    def serial(self) -> str | None:
        return self.attributes.get("serial")

    @property
    def build(self) -> str | None:
        return self.attributes.get("build")

    @property
    def servicepack(self) -> str | None:
        return self.attributes.get("servicepack")

    @property
    def uefi(self) -> bool | None:
        return self.attributes.get("uefi")

    @property
    def hypervisor(self) -> bool | None:
        return self.attributes.get("hypervisor")

    @property
    def remoteSession(self) -> bool | None:
        return self.attributes.get("remoteSession")

    @property
    def idle_time(self) -> int | None:
        return self.attributes.get("idleTime")

    @property
    def users(self) -> List[Users] | None:
        return [Users(x) for x in self.attributes.get("users", [])]
