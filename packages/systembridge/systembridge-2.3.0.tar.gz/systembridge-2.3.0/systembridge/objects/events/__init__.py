"""
Class object for Events
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations
from typing import Any

from ...objects.base import BridgeBase


class Event(BridgeBase):
    @property
    def name(self) -> str:
        return self.attributes.get("name")

    @property
    def data(self) -> Any:
        return self.attributes.get("data")


class EventData(BridgeBase):
    @property
    def api_key(self) -> str:
        return self.attributes.get("api-key")

    @property
    def data(self) -> Event | None:
        return self.attributes.get("data")


class EventBase(BridgeBase):
    @property
    def event(self) -> str:
        return self.attributes.get("event")

    @property
    def data(self) -> Any | EventData:
        return self.attributes.get("data")
