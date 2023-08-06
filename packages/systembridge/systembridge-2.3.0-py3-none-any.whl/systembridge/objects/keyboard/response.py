"""
Class object for KeyboardResponse
Documentation: https://system-bridge.timmo.dev
"""
from .payload import KeyboardPayload


class KeyboardResponse(KeyboardPayload):
    def __init__(self, payload=None):
        super().__init__(payload)
