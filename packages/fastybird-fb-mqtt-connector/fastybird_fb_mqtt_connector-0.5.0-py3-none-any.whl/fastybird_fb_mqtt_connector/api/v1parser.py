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
FastyBird MQTT connector api module parser for API v1
"""

# Python base dependencies
import re
from typing import List, Optional, Tuple

# Library libs
from fastybird_fb_mqtt_connector.api.v1validator import V1Validator
from fastybird_fb_mqtt_connector.consumers.entities import (
    BaseEntity,
    ChannelAttributeEntity,
    ChannelPropertyEntity,
    DeviceAttributeEntity,
    DevicePropertyEntity,
    FirmwareEntity,
    HardwareEntity,
    PropertyAttributeEntity,
)
from fastybird_fb_mqtt_connector.exceptions import ParsePayloadException


class V1Parser:
    """
    MQTT topic parser

    @package        FastyBird:FbMqttConnector!
    @module         api/v1parser

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    @staticmethod
    def parse_message(topic: str, payload: str, retained: bool = False) -> BaseEntity:
        """Parse received message topic & value"""
        if V1Validator.validate(topic=topic) is False:
            raise ParsePayloadException("Provided topic is not valid")

        is_child = V1Validator.validate_child_device_part(topic=topic)

        if V1Validator.validate_device_attribute(topic=topic):
            device_attribute = V1Parser.parse_device_attribute(
                topic=topic,
                payload=payload,
                is_child=is_child,
            )
            device_attribute.retained = retained

            return device_attribute

        if V1Validator.validate_device_hardware_info(topic=topic):
            device_hardware = V1Parser.parse_device_hardware_info(
                topic=topic,
                payload=payload,
                is_child=is_child,
            )
            device_hardware.retained = retained

            return device_hardware

        if V1Validator.validate_device_firmware_info(topic=topic):
            device_firmware = V1Parser.parse_device_firmware_info(
                topic=topic,
                payload=payload,
                is_child=is_child,
            )
            device_firmware.retained = retained

            return device_firmware

        if V1Validator.validate_device_property(topic=topic):
            device_property = V1Parser.parse_device_property(
                topic=topic,
                payload=payload,
                is_child=is_child,
            )
            device_property.retained = retained

            return device_property

        if V1Validator.validate_channel_part(topic=topic):
            if is_child:
                result = re.findall(V1Validator.CHILD_DEVICE_CHANNEL_PARTIAL_REGEXP, topic)
                parent, device, channel = result.pop()

            else:
                result = re.findall(V1Validator.CHANNEL_PARTIAL_REGEXP, topic)
                device, channel = result.pop()
                parent = None

            return V1Parser.parse_channel_message(
                device=device,
                channel=channel,
                parent=parent,
                topic=topic,
                payload=payload,
                retained=retained,
            )

        raise ParsePayloadException("Provided topic is not valid")

    # -----------------------------------------------------------------------------

    @staticmethod
    def parse_channel_message(  # pylint: disable=too-many-arguments
        device: str,
        channel: str,
        parent: Optional[str],
        topic: str,
        payload: str,
        retained: bool = False,
    ) -> BaseEntity:
        """Parse received message topic & value for device channel"""
        if V1Validator.validate_channel_attribute(topic=topic):
            channel_attribute = V1Parser.parse_channel_attribute(
                device=device,
                parent=parent,
                channel=channel,
                topic=topic,
                payload=payload,
            )
            channel_attribute.retained = retained

            return channel_attribute

        if V1Validator.validate_channel_property(topic=topic):
            channel_property = V1Parser.parse_channel_property(
                device=device,
                parent=parent,
                channel=channel,
                topic=topic,
                payload=payload,
            )
            channel_property.retained = retained

            return channel_property

        raise ParsePayloadException("Provided topic is not valid")

    # -----------------------------------------------------------------------------

    @staticmethod
    def parse_device_attribute(
        topic: str,
        payload: str,
        is_child: bool = False,
    ) -> DeviceAttributeEntity:
        """Parse device attribute topic & value"""
        if is_child is True:
            result = re.findall(V1Validator.CHILD_DEVICE_CHANNEL_PARTIAL_REGEXP, topic)
            parent, device, attribute = result.pop()

        else:
            result = re.findall(V1Validator.DEVICE_ATTRIBUTE_REGEXP, topic)
            device, attribute = result.pop()
            parent = None

        return DeviceAttributeEntity(
            device=device,
            attribute=attribute,
            value=payload,
            parent=parent,
        )

    # -----------------------------------------------------------------------------

    @staticmethod
    def parse_device_hardware_info(
        topic: str,
        payload: str,
        is_child: bool = False,
    ) -> HardwareEntity:
        """Parse device hardware info topic & value"""
        if is_child is True:
            result = re.findall(V1Validator.DEVICE_CHILD_HW_INFO_REGEXP, topic)
            parent, device, hardware = result.pop()

        else:
            result = re.findall(V1Validator.DEVICE_ATTRIBUTE_REGEXP, topic)
            device, hardware = result.pop()
            parent = None

        return HardwareEntity(
            device=device,
            parameter=hardware,
            value=payload,
            parent=parent,
        )

    # -----------------------------------------------------------------------------

    @staticmethod
    def parse_device_firmware_info(
        topic: str,
        payload: str,
        is_child: bool = False,
    ) -> FirmwareEntity:
        """Parse device firmware info topic & value"""
        if is_child is True:
            result = re.findall(V1Validator.DEVICE_CHILD_FW_INFO_REGEXP, topic)
            parent, device, firmware = result.pop()

        else:
            result = re.findall(V1Validator.DEVICE_FW_INFO_REGEXP, topic)
            device, firmware = result.pop()
            parent = None

        return FirmwareEntity(
            device=device,
            parameter=firmware,
            value=payload,
            parent=parent,
        )

    # -----------------------------------------------------------------------------

    @staticmethod
    def parse_device_property(
        topic: str,
        payload: str,
        is_child: bool = False,
    ) -> DevicePropertyEntity:
        """Parse device property topic & value"""
        if is_child is True:
            result = re.findall(V1Validator.DEVICE_CHILD_PROPERTY_REGEXP, topic)
            parent, device, name, _, attribute = result.pop()

        else:
            result = re.findall(V1Validator.DEVICE_PROPERTY_REGEXP, topic)
            device, name, _, attribute = result.pop()
            parent = None

        entity = DevicePropertyEntity(
            device=device,
            name=name,
            parent=parent,
        )

        if attribute:
            entity.add_attribute(PropertyAttributeEntity(attribute=attribute, value=payload))

        else:
            entity.value = payload

        return entity

    # -----------------------------------------------------------------------------

    @staticmethod
    def parse_channel_attribute(  # pylint: disable=too-many-arguments
        device: str,
        parent: Optional[str],
        channel: str,
        topic: str,
        payload: str,
    ) -> ChannelAttributeEntity:
        """Parse channel control attribute & value"""
        result: List[Tuple[str, str, str]] = re.findall(V1Validator.CHANNEL_ATTRIBUTE_REGEXP, topic)
        _, __, attribute = result.pop()

        return ChannelAttributeEntity(
            device=device,
            channel=channel,
            attribute=attribute,
            value=payload,
            parent=parent,
        )

    # -----------------------------------------------------------------------------

    @staticmethod
    def parse_channel_property(  # pylint: disable=too-many-arguments
        device: str,
        parent: Optional[str],
        channel: str,
        topic: str,
        payload: str,
    ) -> ChannelPropertyEntity:
        """Parse channel property topic & value"""
        result: List[Tuple[str, str, str, str, str]] = re.findall(V1Validator.CHANNEL_PROPERTY_REGEXP, topic)
        _, __, name, ___, attribute = result.pop()

        entity = ChannelPropertyEntity(
            device=device,
            channel=channel,
            name=name,
            parent=parent,
        )

        if attribute:
            entity.add_attribute(PropertyAttributeEntity(attribute=attribute, value=payload))

        else:
            entity.value = payload

        return entity
