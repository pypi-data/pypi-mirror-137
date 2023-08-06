#!/usr/bin/python3

#     Copyright 2021. FastyBird s.r.o.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

"""
FastyBird MQTT connector entities module
"""

# Python base dependencies
from typing import Dict, List, Optional, Union

# Library dependencies
from fastybird_devices_module.entities.connector import ConnectorEntity
from fastybird_devices_module.entities.device import DeviceEntity

# Library libs
from fastybird_fb_mqtt_connector.types import CONNECTOR_NAME, DEVICE_NAME


class FbMqttConnectorEntity(ConnectorEntity):
    """
    FastyBird MQTT connector entity

    @package        FastyBird:FbMqttConnector!
    @module         entities/connector

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __mapper_args__ = {"polymorphic_identity": CONNECTOR_NAME}

    # -----------------------------------------------------------------------------

    @property
    def type(self) -> str:
        """Connector type"""
        return CONNECTOR_NAME

    # -----------------------------------------------------------------------------

    @property
    def server(self) -> str:
        """Connector server address"""
        return (
            str(self.params.get("server", "127.0.0.1"))
            if self.params is not None and self.params.get("server", "127.0.0.1") is not None
            else "127.0.0.1"
        )

    # -----------------------------------------------------------------------------

    @server.setter
    def server(self, server: Optional[str]) -> None:
        """Connector server address setter"""
        if self.params is not None and bool(self.params) is True:
            self.params["server"] = server

        else:
            self.params = {"server": server}

    # -----------------------------------------------------------------------------

    @property
    def port(self) -> int:
        """Connector server port"""
        return (
            int(str(self.params.get("port", 1883)))
            if self.params is not None and self.params.get("port", 1883) is not None
            else 1883
        )

    # -----------------------------------------------------------------------------

    @port.setter
    def port(self, port: Optional[int]) -> None:
        """Connector server port setter"""
        if self.params is not None and bool(self.params) is True:
            self.params["port"] = port

        else:
            self.params = {"port": port}

    # -----------------------------------------------------------------------------

    @property
    def secured_port(self) -> int:
        """Connector server secured port"""
        return (
            int(str(self.params.get("secured_port", 8883)))
            if self.params is not None and self.params.get("secured_port", 8883) is not None
            else 8883
        )

    # -----------------------------------------------------------------------------

    @secured_port.setter
    def secured_port(self, port: Optional[int]) -> None:
        """Connector server secured port setter"""
        if self.params is not None and bool(self.params) is True:
            self.params["secured_port"] = port

        else:
            self.params = {"secured_port": port}

    # -----------------------------------------------------------------------------

    @property
    def username(self) -> Optional[str]:
        """Connector server username"""
        return (
            str(self.params.get("username", None))
            if self.params is not None and self.params.get("username") is not None
            else None
        )

    # -----------------------------------------------------------------------------

    @username.setter
    def username(self, username: Optional[str]) -> None:
        """Connector server username setter"""
        if self.params is not None and bool(self.params) is True:
            self.params["username"] = username

        else:
            self.params = {"username": username}

    # -----------------------------------------------------------------------------

    @property
    def password(self) -> Optional[str]:
        """Connector server password"""
        return (
            str(self.params.get("password", None))
            if self.params is not None and self.params.get("password") is not None
            else None
        )

    # -----------------------------------------------------------------------------

    @password.setter
    def password(self, password: Optional[str]) -> None:
        """Connector server password setter"""
        if self.params is not None and bool(self.params) is True:
            self.params["password"] = password

        else:
            self.params = {"password": password}

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, int, bool, List[str], None]]:
        """Transform entity to dictionary"""
        return {
            **super().to_dict(),
            **{
                "server": self.server,
                "port": self.port,
                "secured_port": self.secured_port,
                "username": self.username,
            },
        }


class FbMqttDeviceEntity(DeviceEntity):  # pylint: disable=too-few-public-methods
    """
    FastyBird MQTT device entity

    @package        FastyBird:FbMqttConnector!
    @module         entities

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __mapper_args__ = {"polymorphic_identity": DEVICE_NAME}

    # -----------------------------------------------------------------------------

    @property
    def type(self) -> str:
        """Device type"""
        return DEVICE_NAME
