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
FastyBird MQTT connector consumers module devices messages consumers
"""

# Python base dependencies
import logging
import uuid
from typing import List, Union

# Library dependencies
from fastybird_metadata.devices_module import ConnectionState
from kink import inject

# Library libs
from fastybird_fb_mqtt_connector.consumers.consumer import IConsumer
from fastybird_fb_mqtt_connector.consumers.entities import (
    BaseEntity,
    DeviceAttributeEntity,
    FirmwareEntity,
    HardwareEntity,
)
from fastybird_fb_mqtt_connector.logger import Logger
from fastybird_fb_mqtt_connector.registry.model import (
    ChannelsRegistry,
    DevicesPropertiesRegistry,
    DevicesRegistry,
)
from fastybird_fb_mqtt_connector.registry.records import DeviceRecord


@inject(alias=IConsumer)
class DeviceAttributeItemConsumer(IConsumer):  # pylint: disable=too-few-public-methods
    """
    Device attribute message consumer

    @package        FastyBird:FbMqttConnector!
    @module         consumers/device

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __devices_registry: DevicesRegistry
    __properties_registry: DevicesPropertiesRegistry
    __channels_registry: ChannelsRegistry

    __logger: Union[Logger, logging.Logger]

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        devices_registry: DevicesRegistry,
        properties_registry: DevicesPropertiesRegistry,
        channels_registry: ChannelsRegistry,
        logger: Union[Logger, logging.Logger] = logging.getLogger("dummy"),
    ) -> None:
        self.__devices_registry = devices_registry
        self.__properties_registry = properties_registry
        self.__channels_registry = channels_registry

        self.__logger = logger

    # -----------------------------------------------------------------------------

    def consume(self, entity: BaseEntity) -> None:
        """Consume received message"""
        if not isinstance(entity, DeviceAttributeEntity):
            return

        device = self.__devices_registry.get_by_identifier(device_identifier=entity.device)

        if device is None:
            self.__logger.error("Message is for unknown device %s", entity.device)

            return

        if entity.attribute == DeviceAttributeEntity.STATE and ConnectionState.has_value(str(entity.value)):
            self.__devices_registry.set_state(device=device, state=ConnectionState(str(entity.value)))

        else:
            to_update = {
                "device_id": device.id,
                "device_identifier": device.identifier,
                "device_name": device.name,
                "device_enabled": device.enabled,
                "device_state": device.state,
                "hardware_manufacturer": device.hardware_manufacturer,
                "hardware_model": device.hardware_model,
                "hardware_version": device.hardware_version,
                "firmware_manufacturer": device.firmware_manufacturer,
                "firmware_version": device.firmware_version,
                "controls": device.controls,
            }

            if entity.attribute == DeviceAttributeEntity.NAME:
                to_update["device_name"] = str(entity.value)

            if entity.attribute == DeviceAttributeEntity.CONTROLS and isinstance(entity.value, list):
                to_update["controls"] = entity.value

            if entity.attribute == DeviceAttributeEntity.PROPERTIES and isinstance(entity.value, list):
                self.__process_properties(device=device, values=entity.value)

            if entity.attribute == DeviceAttributeEntity.CHANNELS and isinstance(entity.value, list):
                self.__process_channels(device=device, values=entity.value)

            self.__devices_registry.update(**to_update)  # type: ignore[arg-type]

        self.__logger.debug("Consumed device attribute message for: %s", device.identifier)

    # -----------------------------------------------------------------------------

    def __process_properties(self, device: DeviceRecord, values: List) -> None:
        for identifier in values:
            device_property = self.__properties_registry.get_by_identifier(
                device_id=device.id,
                property_identifier=identifier,
            )

            if device_property is None:
                self.__properties_registry.create_or_update(
                    device_id=device.id,
                    property_id=uuid.uuid4(),
                    property_identifier=identifier,
                )

        for device_property in self.__properties_registry.get_all_for_device(device_id=device.id):
            if device_property.identifier not in values:
                self.__properties_registry.remove(property_id=device_property.id)

    # -----------------------------------------------------------------------------

    def __process_channels(self, device: DeviceRecord, values: List) -> None:
        for identifier in values:
            channel = self.__channels_registry.get_by_identifier(
                device_id=device.id,
                channel_identifier=identifier,
            )

            if channel is None:
                self.__channels_registry.create_or_update(
                    device_id=device.id,
                    channel_id=uuid.uuid4(),
                    channel_identifier=identifier,
                )

        for channel in self.__channels_registry.get_all_by_device(device_id=device.id):
            if channel.identifier not in values:
                self.__channels_registry.remove(channel_id=channel.id)


@inject(alias=IConsumer)
class DeviceHardwareItemConsumer(IConsumer):  # pylint: disable=too-few-public-methods
    """
    Device hardware info message consumer

    @package        FastyBird:FbMqttConnector!
    @module         consumers/device

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __devices_registry: DevicesRegistry

    __logger: Union[Logger, logging.Logger]

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        devices_registry: DevicesRegistry,
        logger: Union[Logger, logging.Logger] = logging.getLogger("dummy"),
    ) -> None:
        self.__devices_registry = devices_registry

        self.__logger = logger

    # -----------------------------------------------------------------------------

    def consume(self, entity: BaseEntity) -> None:
        """Consume received message"""
        if not isinstance(entity, HardwareEntity):
            return

        device = self.__devices_registry.get_by_identifier(device_identifier=entity.device)

        if device is None:
            self.__logger.error("Message is for unknown device %s", entity.device)

            return

        to_update = {
            "device_id": device.id,
            "device_identifier": device.identifier,
            "device_name": device.name,
            "device_enabled": device.enabled,
            "device_state": device.state,
            "hardware_manufacturer": device.hardware_manufacturer,
            "hardware_model": device.hardware_model,
            "hardware_version": device.hardware_version,
            "firmware_manufacturer": device.firmware_manufacturer,
            "firmware_version": device.firmware_version,
            "controls": device.controls,
        }

        if entity.parameter == HardwareEntity.MAC_ADDRESS:
            to_update["hardware_mac_address"] = entity.value

        elif entity.parameter == HardwareEntity.MANUFACTURER:
            to_update["hardware_manufacturer"] = entity.value

        elif entity.parameter == HardwareEntity.MODEL:
            to_update["hardware_model"] = entity.value

        elif entity.parameter == HardwareEntity.VERSION:
            to_update["hardware_version"] = entity.value

        else:
            return

        self.__devices_registry.update(**to_update)  # type: ignore[arg-type]

        self.__logger.debug("Consumed device hardware info message for: %s", device.identifier)


@inject(alias=IConsumer)
class DeviceFirmwareItemConsumer(IConsumer):  # pylint: disable=too-few-public-methods
    """
    Device firmware info message consumer

    @package        FastyBird:FbMqttConnector!
    @module         consumers/device

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __devices_registry: DevicesRegistry

    __logger: Union[Logger, logging.Logger]

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        devices_registry: DevicesRegistry,
        logger: Union[Logger, logging.Logger] = logging.getLogger("dummy"),
    ) -> None:
        self.__devices_registry = devices_registry

        self.__logger = logger

    # -----------------------------------------------------------------------------

    def consume(self, entity: BaseEntity) -> None:
        """Consume received message"""
        if not isinstance(entity, FirmwareEntity):
            return

        device = self.__devices_registry.get_by_identifier(device_identifier=entity.device)

        if device is None:
            self.__logger.error("Message is for unknown device %s", entity.device)

            return

        to_update = {
            "device_id": device.id,
            "device_identifier": device.identifier,
            "device_name": device.name,
            "device_enabled": device.enabled,
            "device_state": device.state,
            "hardware_manufacturer": device.hardware_manufacturer,
            "hardware_model": device.hardware_model,
            "hardware_version": device.hardware_version,
            "firmware_manufacturer": device.firmware_manufacturer,
            "firmware_version": device.firmware_version,
            "controls": device.controls,
        }

        if entity.parameter == FirmwareEntity.MANUFACTURER:
            to_update["firmware_manufacturer"] = entity.value

        elif entity.parameter == FirmwareEntity.VERSION:
            to_update["firmware_version"] = entity.value

        else:
            return

        self.__devices_registry.update(**to_update)  # type: ignore[arg-type]

        self.__logger.debug("Consumed device firmware info message for: %s", device.identifier)
