"""Bridge: Init"""
from __future__ import annotations

from aiohttp import ClientResponse
from typing import Any, List
from urllib.parse import urlencode

from systembridge.objects.hardware_sensor import HardwareSensor

from .client import BridgeClient
from .client_websocket import BridgeClientWebSocket
from .objects.audio import Audio, AudioDevice, AudioSettings
from .objects.audio.put import AudioPutPayload, AudioPutResponse
from .objects.base import BridgeBase
from .objects.battery import Battery
from .objects.bluetooth import Bluetooth
from .objects.command.payload import CommandPayload
from .objects.command.response import CommandResponse
from .objects.cpu import Cache, Cpu, CpuInner, CurrentSpeed, Temperature
from .objects.display import DisplayBase
from .objects.events import Event, EventBase
from .objects.filesystem import BlockDevices, DiskLayout, Filesystem, FsSize
from .objects.filesystem.file import FilesystemFile
from .objects.graphics import Graphics
from .objects.information import Information
from .objects.keyboard.payload import KeyboardPayload
from .objects.keyboard.response import KeyboardResponse
from .objects.memory import Memory
from .objects.network import Network
from .objects.open.payload import OpenPayload
from .objects.os import Os
from .objects.processes import Load, ProcessList, Processes
from .objects.settings import Settings
from .objects.settings.put import SettingsPutPayload
from .objects.system import System

BASE_HEADERS = {"Accept": "application/json"}


class Bridge(BridgeBase):
    """Main class for Bridge."""

    def __init__(self, client: BridgeClient, base_url: str, api_key: str) -> None:
        """Initialize the class."""
        self._client = client
        self._base_url = base_url
        self._api_key = api_key
        self._audio: Audio = None
        self._battery: Battery = None
        self._bluetooth: Bluetooth = None
        self._cpu: Cpu = None
        self._display: DisplayBase = None
        self._filesystem: Filesystem = None
        self._graphics: Graphics = None
        self._information: Information = None
        self._memory: Memory = None
        self._network: Network = None
        self._os: Os = None
        self._processes: Processes = None
        self._settings: List[Settings] = None
        self._system: System = None
        self._websocket_client: BridgeClientWebSocket = None

    @property
    def audio(self) -> Audio:
        return self._audio

    @property
    def battery(self) -> Battery:
        return self._battery

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def bluetooth(self) -> Bluetooth:
        return self._bluetooth

    @property
    def cpu(self) -> Cpu:
        return self._cpu

    @property
    def display(self) -> DisplayBase:
        return self._display

    @property
    def filesystem(self) -> Filesystem:
        return self._filesystem

    @property
    def graphics(self) -> Graphics:
        return self._graphics

    @property
    def information(self) -> Information:
        return self._information

    @property
    def memory(self) -> Memory:
        return self._memory

    @property
    def network(self) -> Network:
        return self._network

    @property
    def os(self) -> Os:
        return self._os

    @property
    def processes(self) -> Processes:
        return self._processes

    @property
    def settings(self) -> List[Settings]:
        return self._settings

    @property
    def system(self) -> System:
        return self._system

    @property
    def websocket_connected(self) -> bool:
        """Check if the websocket is connected"""
        return self._websocket_client is not None and self._websocket_client.connected

    async def async_post(self, path: str, payload: Any | None) -> Any:
        """Generic Delete"""
        response: ClientResponse = await self._client.post(
            f"{self._base_url}{path}",
            headers={**BASE_HEADERS, "api-key": self._api_key},
            json=payload,
        )
        return await response.json()

    async def async_get(self, path: str) -> Any:
        """Generic get"""
        response: ClientResponse = await self._client.get(
            f"{self._base_url}{path}",
            headers={**BASE_HEADERS, "api-key": self._api_key},
        )
        if "application/json" in response.headers.get("Content-Type", ""):
            return await response.json()
        return await response.text()

    async def async_post(self, path: str, payload: Any) -> Any:
        """Generic post"""
        response: ClientResponse = await self._client.post(
            f"{self._base_url}{path}",
            headers={**BASE_HEADERS, "api-key": self._api_key},
            json=payload,
        )
        if "application/json" in response.headers.get("Content-Type", ""):
            return await response.json()
        return await response.text()

    async def async_put(self, path: str, payload: Any) -> Any:
        """Generic put"""
        response: ClientResponse = await self._client.put(
            f"{self._base_url}{path}",
            headers={**BASE_HEADERS, "api-key": self._api_key},
            json=payload,
        )
        if "application/json" in response.headers.get("Content-Type", ""):
            return await response.json()
        return await response.text()

    async def async_get_audio(self) -> Audio:
        """Get audio information"""
        self._audio = Audio(await self.async_get("/audio"))
        return self._audio

    async def async_update_audio(
        self, id: str, payload: AudioPutPayload
    ) -> AudioPutResponse:
        """Update audio"""
        return AudioPutResponse(await self.async_put(f"/audio/{id}", payload))

    async def async_get_battery(self) -> Battery:
        """Get battery information"""
        self._battery = Battery(await self.async_get("/battery"))
        return self._battery

    async def async_get_bluetooth(self) -> Bluetooth:
        """Get bluetooth information"""
        self._bluetooth = Bluetooth(await self.async_get("/bluetooth"))
        return self._bluetooth

    async def async_send_command(self, payload: CommandPayload) -> CommandResponse:
        """Send command"""
        return CommandResponse(await self.async_post("/command", payload))

    async def async_get_cpu(self) -> Cpu:
        """Get cpu information"""
        self._cpu = Cpu(await self.async_get("/cpu"))
        return self._cpu

    async def async_get_display(self) -> DisplayBase:
        """Get display information"""
        self._display = DisplayBase(await self.async_get("/display"))
        return self._display

    async def async_get_filesystem(self) -> Filesystem:
        """Get filesystem information"""
        self._filesystem = Filesystem(await self.async_get("/filesystem"))
        return self._filesystem

    async def async_get_filesystem_files(self, path: str) -> List[FilesystemFile]:
        """Get filesystem files information"""
        files = await self.async_get(f"/filesystem/files?path={path}")
        return [FilesystemFile(file) for file in files]

    async def async_get_filesystem_file(self, path: str) -> FilesystemFile:
        """Get filesystem files information"""
        return FilesystemFile(
            await self.async_get(f"/filesystem/files/file?path={path}")
        )

    async def async_get_filesystem_file_data(self, path: str) -> any:
        """Get filesystem file data"""
        return await self.async_get(f"/filesystem/files/file/data?path={path}")

    def get_filesystem_file_data_url(self, path: str) -> str:
        """Get filesystem file data url"""
        return f"{self._base_url}/filesystem/files/file/data?apiKey={self._api_key}&path={path}"

    async def async_upload_filesystem_file(self, path: str) -> any:
        """Upload file to filesystem"""
        return FilesystemFile(
            await self.async_post(f"/filesystem/files/file/data?path={path}")
        )

    async def async_get_graphics(self) -> Graphics:
        """Get graphics information"""
        self._graphics = Graphics(await self.async_get("/graphics"))
        return self._graphics

    async def async_get_information(self) -> Information:
        """Get information"""
        self._information = Information(await self.async_get("/information"))
        return self._information

    async def async_get_memory(self) -> Memory:
        """Get memory information"""
        self._memory = Memory(await self.async_get("/memory"))
        return self._memory

    async def async_get_network(self) -> Network:
        """Get network information"""
        self._network = Network(await self.async_get("/network"))
        return self._network

    async def async_open(self, payload: OpenPayload) -> OpenPayload:
        """Send command"""
        return OpenPayload(await self.async_post("/open", payload))

    async def async_get_os(self) -> Os:
        """Get os information"""
        self._os = Os(await self.async_get("/os"))
        return self._os

    async def async_get_processes(self) -> Processes:
        """Get processes information"""
        self._processes = Processes(await self.async_get("/processes"))
        return self._processes

    async def async_get_process(self, name: str) -> Processes:
        """Get process from name"""
        self._processes = ProcessList(await self.async_get(f"/processes/{name}"))
        return self._processes

    async def async_get_settings(self) -> List[Settings]:
        """Get settings"""
        settings = await self.async_get("/settings")
        self._settings = [Settings(setting) for setting in settings]
        return self._settings

    async def async_get_setting(self, section: str, key: str) -> Settings:
        """Get setting"""
        return Settings(await self.async_get(f"/settings/{section}/{key}"))

    async def async_update_setting(
        self, section: str, key: str, payload: SettingsPutPayload
    ) -> Settings:
        """Update setting"""
        return Settings(await self.async_put(f"/settings/{section}/{key}", payload))

    async def async_get_system(self) -> System:
        """Get system information"""
        self._system = System(await self.async_get("/system"))
        return self._system

    async def async_send_keypress(self, payload: KeyboardPayload) -> KeyboardResponse:
        """Send keypress"""
        return KeyboardResponse(await self.async_post("/keyboard", payload))

    async def async_connect_websocket(self, host: str, port: int) -> None:
        self._websocket_client: BridgeClientWebSocket = BridgeClientWebSocket(
            self._api_key
        )
        await self._websocket_client.connect(f"ws://{host}:{port}")
        await self._websocket_client.register_listener()

    async def async_close_websocket(self) -> None:
        if self._websocket_client is not None:
            await self._websocket_client.close()

    async def async_send_event(self, event: str, data: Any) -> None:
        await self._websocket_client.send_event(event, data)

    async def listen_for_events(self, callback: function) -> None:
        async def handle_message(message: EventBase) -> None:
            if "data" in message and type(message["data"]) is dict:
                event = Event(message["data"])
                if "data-" in event.name:
                    name = event.name.replace("data-", "")
                    if name == "audio":
                        self._audio = Audio(event.data)
                    if name == "audio-findCurrent":
                        if self._audio is None:
                            self._audio = Audio({"current": event.data})
                        else:
                            self._audio = Audio({**self._audio, "current": event.data})
                    if name == "audio-getDevices":
                        if self._audio is None:
                            self._audio = Audio({"devices": event.data})
                        else:
                            self._audio = Audio({**self._audio, "devices": event.data})
                    elif name == "battery":
                        self._battery = Battery(event.data)
                    elif name == "bluetooth":
                        self._bluetooth = Bluetooth(event.data)
                    elif name == "cpu":
                        self._cpu = Cpu(event.data)
                    elif name == "cpu-findCpuCache":
                        if self._cpu is None:
                            self._cpu = Cpu({"cache": event.data})
                        else:
                            self._cpu = Cpu({**self._cpu, "cache": event.data})
                    elif name == "cpu-findCpu":
                        if self._cpu is None:
                            self._cpu = Cpu({"cpu": event.data})
                        else:
                            self._cpu = Cpu({**self._cpu, "cpu": event.data})
                    elif name == "cpu-findCurrentSpeed":
                        if self._cpu is None:
                            self._cpu = Cpu({"currentSpeed": event.data})
                        else:
                            self._cpu = Cpu({**self._cpu, "currentSpeed": event.data})
                    elif name == "cpu-findTemperature":
                        if self._cpu is None:
                            self._cpu = Cpu({"temperature": event.data})
                        else:
                            self._cpu = Cpu({**self._cpu, "temperature": event.data})
                    elif name == "cpu-findHardwareSensors":
                        if self._cpu is None:
                            self._cpu = Cpu({"hardwareSensors": event.data})
                        else:
                            self._cpu = Cpu(
                                {**self._cpu, "hardwareSensors": event.data}
                            )
                    elif name == "display":
                        self._display = DisplayBase(event.data)
                    elif name == "filesystem":
                        self._filesystem = Filesystem(event.data)
                    elif name == "filesystem-findBlockDevices":
                        if self._filesystem is None:
                            self._filesystem = Filesystem({"blockDevices": event.data})
                        else:
                            self._filesystem = Filesystem(
                                {**self._filesystem, "blockDevices": event.data}
                            )
                    elif name == "filesystem-findDisksLayout":
                        if self._filesystem is None:
                            self._filesystem = Filesystem({"diskLayout": event.data})
                        else:
                            self._filesystem = Filesystem(
                                {**self._filesystem, "diskLayout": event.data}
                            )
                    elif name == "filesystem-findDisksIO":
                        if self._filesystem is None:
                            self._filesystem = Filesystem({"disksIO": event.data})
                        else:
                            self._filesystem = Filesystem(
                                {**self._filesystem, "disksIO": event.data}
                            )
                    elif name == "filesystem-findSizes":
                        if self._filesystem is None:
                            self._filesystem = Filesystem({"fsSize": event.data})
                        else:
                            self._filesystem = Filesystem(
                                {**self._filesystem, "fsSize": event.data}
                            )
                    elif name == "graphics":
                        self._graphics = Graphics(event.data)
                    elif name == "information":
                        self._information = Information(event.data)
                    elif name == "memory":
                        self._memory = Memory(event.data)
                    elif name == "network":
                        self._network = Network(event.data)
                    elif name == "os":
                        self._os = Os(event.data)
                    elif name == "processes":
                        self._processes = Processes(event.data)
                    elif name == "processes-findCurrentLoad":
                        if self._processes is None:
                            self._processes = Processes({"load": event.data})
                        else:
                            self._processes = Processes(
                                {**self._processes, "load": event.data}
                            )
                    elif name == "settings":
                        self._settings = [Settings(setting) for setting in event.data]
                    elif name == "system":
                        self._system = System(event.data)
                await callback(event)

        await self._websocket_client.listen_for_messages(handle_message)

    def get_configuration_url(self, include_api_key=False) -> str:
        """Get configuration url"""
        return f"""{self.base_url}/app/settings?{urlencode({
            "apiKey": self._api_key if include_api_key is not False else "",
            "apiPort": self.information.apiPort
            if self.information is not None
            else "",
            "wsPort": self.information.websocketPort
            if self.information is not None
            else "",
        })}"""
