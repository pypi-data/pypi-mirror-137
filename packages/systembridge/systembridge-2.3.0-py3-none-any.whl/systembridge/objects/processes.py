"""
Class object for Processes
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations
from typing import List

from .base import BridgeBase


class ProcessList(BridgeBase):
    @property
    def pid(self) -> int | None:
        return self.attributes.get("pid")

    @property
    def parentPid(self) -> int | None:
        return self.attributes.get("parentPid")

    @property
    def name(self) -> str | None:
        return self.attributes.get("name")

    @property
    def cpu(self) -> float | None:
        return self.attributes.get("cpu")

    @property
    def cpuu(self) -> float | None:
        return self.attributes.get("cpuu")

    @property
    def cpus(self) -> float | None:
        return self.attributes.get("cpus")

    @property
    def mem(self) -> float | None:
        return self.attributes.get("mem")

    @property
    def priority(self) -> int | float | None:
        return self.attributes.get("priority")

    @property
    def memVsz(self) -> int | float | None:
        return self.attributes.get("memVsz")

    @property
    def memRss(self) -> int | float | None:
        return self.attributes.get("memRss")

    @property
    def nice(self) -> int | float | None:
        return self.attributes.get("nice")

    @property
    def started(self) -> str | None:
        return self.attributes.get("started")

    @property
    def state(self) -> str | None:
        return self.attributes.get("state")

    @property
    def tty(self) -> str | None:
        return self.attributes.get("tty")

    @property
    def user(self) -> str | None:
        return self.attributes.get("user")

    @property
    def command(self) -> str | None:
        return self.attributes.get("command")

    @property
    def params(self) -> str | None:
        return self.attributes.get("params")

    @property
    def path(self) -> str | None:
        return self.attributes.get("path")


class Cpus(BridgeBase):
    @property
    def load(self) -> float | None:
        return self.attributes.get("load")

    @property
    def loadUser(self) -> float | None:
        return self.attributes.get("loadUser")

    @property
    def loadSystem(self) -> float | None:
        return self.attributes.get("loadSystem")

    @property
    def loadNice(self) -> float | None:
        return self.attributes.get("loadNice")

    @property
    def loadIdle(self) -> float | None:
        return self.attributes.get("loadIdle")

    @property
    def loadIrq(self) -> float | None:
        return self.attributes.get("loadIrq")

    @property
    def rawLoad(self) -> float | None:
        return self.attributes.get("rawLoad")

    @property
    def rawLoadUser(self) -> float | None:
        return self.attributes.get("rawLoadUser")

    @property
    def rawLoadSystem(self) -> float | None:
        return self.attributes.get("rawLoadSystem")

    @property
    def rawLoadNice(self) -> float | None:
        return self.attributes.get("rawLoadNice")

    @property
    def rawLoadIdle(self) -> float | None:
        return self.attributes.get("rawLoadIdle")

    @property
    def rawLoadIrq(self) -> float | None:
        return self.attributes.get("rawLoadIrq")


class Load(BridgeBase):
    @property
    def avgLoad(self) -> float | None:
        return self.attributes.get("avgLoad")

    @property
    def currentLoad(self) -> float | None:
        return self.attributes.get("currentLoad")

    @property
    def currentLoadUser(self) -> float | None:
        return self.attributes.get("currentLoadUser")

    @property
    def currentLoadSystem(self) -> float | None:
        return self.attributes.get("currentLoadSystem")

    @property
    def currentLoadNice(self) -> float | None:
        return self.attributes.get("currentLoadNice")

    @property
    def currentLoadIdle(self) -> float | None:
        return self.attributes.get("currentLoadIdle")

    @property
    def currentLoadIrq(self) -> float | None:
        return self.attributes.get("currentLoadIrq")

    @property
    def rawCurrentLoad(self) -> float | None:
        return self.attributes.get("rawCurrentLoad")

    @property
    def rawCurrentLoadUser(self) -> float | None:
        return self.attributes.get("rawCurrentLoadUser")

    @property
    def rawCurrentLoadSystem(self) -> float | None:
        return self.attributes.get("rawCurrentLoadSystem")

    @property
    def rawCurrentLoadNice(self) -> float | None:
        return self.attributes.get("rawCurrentLoadNice")

    @property
    def rawCurrentLoadIdle(self) -> float | None:
        return self.attributes.get("rawCurrentLoadIdle")

    @property
    def rawCurrentLoadIrq(self) -> float | None:
        return self.attributes.get("rawCurrentLoadIrq")

    @property
    def cpus(self) -> List[Cpus] | None:
        return [Cpus(x) for x in self.attributes.get("cpus", [])]


class Processes(BridgeBase):
    @property
    def all(self):
        return self.attributes.get("all")

    @property
    def running(self):
        return self.attributes.get("running")

    @property
    def blocked(self):
        return self.attributes.get("blocked")

    @property
    def sleeping(self):
        return self.attributes.get("sleeping")

    @property
    def unknown(self):
        return self.attributes.get("unknown")

    @property
    def ProcessList(self):
        return [ProcessList(x) for x in self.attributes.get("list", [])]

    @property
    def load(self):
        return Load(self.attributes.get("load", {}))
