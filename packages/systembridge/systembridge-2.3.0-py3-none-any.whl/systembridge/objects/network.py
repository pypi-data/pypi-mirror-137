"""
Class object for Network
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations

from typing import Dict, List
from .base import BridgeBase


class Connections(BridgeBase):
    @property
    def protocol(self) -> str | None:
        return self.attributes.get("protocol")

    @property
    def localAddress(self) -> str | None:
        return self.attributes.get("localAddress")

    @property
    def localPort(self) -> str | None:
        return self.attributes.get("localPort")

    @property
    def peerAddress(self) -> str | None:
        return self.attributes.get("peerAddress")

    @property
    def peerPort(self) -> str | None:
        return self.attributes.get("peerPort")

    @property
    def state(self) -> str | None:
        return self.attributes.get("state")

    @property
    def pid(self) -> str | None:
        return self.attributes.get("pid")

    @property
    def process(self) -> str | None:
        return self.attributes.get("process")


class Interface(BridgeBase):
    @property
    def iface(self) -> str | None:
        return self.attributes.get("iface")

    @property
    def ifaceName(self) -> str | None:
        return self.attributes.get("ifaceName")

    @property
    def ip4(self) -> str | None:
        return self.attributes.get("ip4")

    @property
    def ip4subnet(self) -> str | None:
        return self.attributes.get("ip4subnet")

    @property
    def ip6(self) -> str | None:
        return self.attributes.get("ip6")

    @property
    def ip6subnet(self) -> str | None:
        return self.attributes.get("ip6subnet")

    @property
    def mac(self) -> str | None:
        return self.attributes.get("mac")

    @property
    def internal(self) -> bool | None:
        return self.attributes.get("internal")

    @property
    def virtual(self) -> bool | None:
        return self.attributes.get("virtual")

    @property
    def operstate(self) -> str | None:
        return self.attributes.get("operstate")

    @property
    def type(self) -> str | None:
        return self.attributes.get("type")

    @property
    def duplex(self) -> str | None:
        return self.attributes.get("duplex")

    @property
    def mtu(self) -> str | None:
        return self.attributes.get("mtu")

    @property
    def speed(self) -> int | None:
        return self.attributes.get("speed")

    @property
    def dhcp(self) -> bool | None:
        return self.attributes.get("dhcp")

    @property
    def dnsSuffix(self) -> str | None:
        return self.attributes.get("dnsSuffix")

    @property
    def ieee8021xAuth(self) -> str | None:
        return self.attributes.get("ieee8021xAuth")

    @property
    def ieee8021xState(self) -> str | None:
        return self.attributes.get("ieee8021xState")

    @property
    def carrierChanges(self) -> int | None:
        return self.attributes.get("carrierChanges")


class Stat(BridgeBase):
    @property
    def iface(self) -> str | None:
        return self.attributes.get("iface")

    @property
    def operstate(self) -> str | None:
        return self.attributes.get("operstate")

    @property
    def rx_bytes(self) -> int | None:
        return self.attributes.get("rx_bytes")

    @property
    def rx_dropped(self) -> int | None:
        return self.attributes.get("rx_dropped")

    @property
    def rx_errors(self) -> int | None:
        return self.attributes.get("rx_errors")

    @property
    def tx_bytes(self) -> int | None:
        return self.attributes.get("tx_bytes")

    @property
    def tx_dropped(self) -> int | None:
        return self.attributes.get("tx_dropped")

    @property
    def tx_errors(self) -> int | None:
        return self.attributes.get("tx_errors")

    @property
    def rx_sec(self) -> int | None:
        return self.attributes.get("rx_sec")

    @property
    def tx_sec(self) -> int | None:
        return self.attributes.get("tx_sec")

    @property
    def ms(self) -> int | None:
        return self.attributes.get("ms")


class Network(BridgeBase):
    @property
    def connections(self) -> List[Connections] | None:
        return [Connections(x) for x in self.attributes.get("connections", [])]

    @property
    def gatewayDefault(self) -> str | None:
        return self.attributes.get("gatewayDefault")

    @property
    def interfaceDefault(self) -> str | None:
        return self.attributes.get("interfaceDefault")

    @property
    def interfaces(self) -> Dict[str, Interface] | None:
        return self.attributes.get("interfaces")

    @property
    def stats(self) -> Dict[str, Stat] | None:
        return self.attributes.get("stats")
