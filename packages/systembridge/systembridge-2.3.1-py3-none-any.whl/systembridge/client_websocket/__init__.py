"""Bridge: ClientWebSocket"""
from __future__ import annotations
import asyncio
import json
import websockets

from typing import Any
from websockets import ConnectionClosed, InvalidHandshake, InvalidMessage

from ..exceptions import (
    BridgeConnectionClosedException,
    BridgeException,
)
from ..objects.base import BridgeBase


class BridgeClientWebSocket(BridgeBase):
    """Client to handle websocket communication."""

    def __init__(self, api_key: str) -> None:
        self._api_key: str = api_key
        self._websocket = None

    @property
    def websocket(self):
        """Get websocket connection."""
        return self._websocket

    @property
    def connected(self) -> bool:
        """Get connection state."""
        return self._websocket is not None and not self._websocket.closed

    async def connect(self, uri: str) -> None:
        try:
            self._websocket = await websockets.connect(uri)
        except InvalidHandshake as e:
            raise BridgeException from e

    async def close(self) -> None:
        if self._websocket is not None:
            await self._websocket.close()
            self._websocket = None

    async def register_listener(self) -> None:
        try:
            await self._websocket.send(
                json.dumps(
                    {
                        "event": "register-listener",
                        "data": {"api-key": self._api_key},
                    }
                )
            )
        except ConnectionClosed as e:
            raise BridgeConnectionClosedException from e
        except (InvalidMessage, InvalidHandshake) as e:
            raise BridgeException from e

    async def send_event(self, event: str, data: Any | None) -> None:
        try:
            await self._websocket.send(
                json.dumps(
                    {
                        "event": "events",
                        "data": {
                            "api-key": self._api_key,
                            "data": {
                                "name": event,
                                "data": data,
                            },
                        },
                    }
                )
            )
        except ConnectionClosed as e:
            raise BridgeConnectionClosedException from e
        except (InvalidMessage, InvalidHandshake) as e:
            raise BridgeException from e

    async def listen_for_messages(self, callback: function) -> None:
        while True:
            await asyncio.sleep(0)
            try:
                message = await self._websocket.recv()
                await callback(json.loads(message))
            except ConnectionClosed as e:
                raise BridgeConnectionClosedException from e
