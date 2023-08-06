"""
Class object for FilesystemFile
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from ..base import BridgeBase


class FilesystemFile(BridgeBase):
    @property
    def name(self) -> str:
        return self.attributes.get("name")

    @property
    def created(self) -> str | None:
        return self.attributes.get("created")

    @property
    def extension(self) -> str | None:
        return self.attributes.get("extension")

    @property
    def isDirectory(self) -> bool | None:
        return self.attributes.get("isDirectory")

    @property
    def isFile(self) -> bool | None:
        return self.attributes.get("isFile")

    @property
    def isLink(self) -> bool | None:
        return self.attributes.get("isLink")

    @property
    def lastAccessed(self) -> str | None:
        return self.attributes.get("lastAccessed")

    @property
    def lastModified(self) -> str | None:
        return self.attributes.get("lastModified")

    @property
    def mimeType(self) -> str | None:
        return self.attributes.get("mimeType")

    @property
    def size(self) -> int | None:
        return self.attributes.get("size")
