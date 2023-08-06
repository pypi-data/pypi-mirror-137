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
FastyBird MQTT connector events module listeners
"""

# Python base dependencies
import logging
import uuid
from typing import Optional, Union

# Library dependencies
from fastybird_devices_module.entities.channel import ChannelDynamicPropertyEntity
from fastybird_devices_module.entities.device import (
    DeviceDynamicPropertyEntity,
    DeviceStaticPropertyEntity,
)
from fastybird_devices_module.managers.channel import (
    ChannelControlsManager,
    ChannelPropertiesManager,
    ChannelsManager,
)
from fastybird_devices_module.managers.device import (
    DeviceControlsManager,
    DevicePropertiesManager,
    DevicesManager,
)
from fastybird_devices_module.managers.state import (
    IChannelPropertiesStatesManager,
    IDevicePropertiesStatesManager,
)
from fastybird_devices_module.repositories.channel import (
    ChannelsControlsRepository,
    ChannelsPropertiesRepository,
    ChannelsRepository,
)
from fastybird_devices_module.repositories.device import (
    DevicesControlsRepository,
    DevicesPropertiesRepository,
    DevicesRepository,
)
from fastybird_devices_module.repositories.state import (
    IChannelPropertyStateRepository,
    IDevicePropertyStateRepository,
)
from fastybird_metadata.devices_module import ConnectionState, DevicePropertyName
from fastybird_metadata.types import DataType
from kink import inject
from whistle import Event, EventDispatcher

# Library libs
from fastybird_fb_mqtt_connector.events.events import (
    ChannelPropertyActualValueEvent,
    ChannelPropertyRecordCreatedOrUpdatedEvent,
    ChannelPropertyRecordDeletedEvent,
    ChannelRecordCreatedOrUpdatedEvent,
    ChannelRecordDeletedEvent,
    DevicePropertyActualValueEvent,
    DevicePropertyRecordCreatedOrUpdatedEvent,
    DevicePropertyRecordDeletedEvent,
    DeviceRecordCreatedOrUpdatedEvent,
    DeviceStateChangedEvent,
)
from fastybird_fb_mqtt_connector.logger import Logger
from fastybird_fb_mqtt_connector.registry.records import DeviceRecord


@inject(
    bind={
        "devices_properties_states_repository": IDevicePropertyStateRepository,
        "devices_properties_states_manager": IDevicePropertiesStatesManager,
        "channels_properties_states_repository": IChannelPropertyStateRepository,
        "channels_properties_states_manager": IChannelPropertiesStatesManager,
    }
)
class EventsListener:  # pylint: disable=too-many-instance-attributes
    """
    Events listener

    @package        FastyBird:FbMqttConnector!
    @module         events/listeners

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __connector_id: uuid.UUID

    __devices_repository: DevicesRepository
    __devices_manager: DevicesManager

    __devices_properties_repository: DevicesPropertiesRepository
    __devices_properties_manager: DevicePropertiesManager
    __devices_properties_states_repository: Optional[IDevicePropertyStateRepository] = None
    __devices_properties_states_manager: Optional[IDevicePropertiesStatesManager] = None

    __devices_controls_repository: DevicesControlsRepository
    __devices_controls_manager: DeviceControlsManager

    __channels_repository: ChannelsRepository
    __channels_manager: ChannelsManager

    __channels_properties_repository: ChannelsPropertiesRepository
    __channels_properties_manager: ChannelPropertiesManager
    __channels_properties_states_repository: Optional[IChannelPropertyStateRepository] = None
    __channels_properties_states_manager: Optional[IChannelPropertiesStatesManager] = None

    __channels_controls_repository: ChannelsControlsRepository
    __channels_controls_manager: ChannelControlsManager

    __event_dispatcher: EventDispatcher

    __logger: Union[Logger, logging.Logger]

    # -----------------------------------------------------------------------------

    def __init__(  # pylint: disable=too-many-arguments,too-many-locals
        self,
        devices_repository: DevicesRepository,
        devices_manager: DevicesManager,
        devices_properties_repository: DevicesPropertiesRepository,
        devices_properties_manager: DevicePropertiesManager,
        devices_controls_repository: DevicesControlsRepository,
        devices_controls_manager: DeviceControlsManager,
        channels_repository: ChannelsRepository,
        channels_manager: ChannelsManager,
        channels_properties_repository: ChannelsPropertiesRepository,
        channels_properties_manager: ChannelPropertiesManager,
        channels_controls_repository: ChannelsControlsRepository,
        channels_controls_manager: ChannelControlsManager,
        event_dispatcher: EventDispatcher,
        devices_properties_states_repository: Optional[IDevicePropertyStateRepository] = None,
        devices_properties_states_manager: Optional[IDevicePropertiesStatesManager] = None,
        channels_properties_states_repository: Optional[IChannelPropertyStateRepository] = None,
        channels_properties_states_manager: Optional[IChannelPropertiesStatesManager] = None,
        logger: Union[Logger, logging.Logger] = logging.getLogger("dummy"),
    ) -> None:
        self.__devices_repository = devices_repository
        self.__devices_manager = devices_manager

        self.__devices_properties_repository = devices_properties_repository
        self.__devices_properties_manager = devices_properties_manager
        self.__devices_properties_states_repository = devices_properties_states_repository
        self.__devices_properties_states_manager = devices_properties_states_manager

        self.__devices_controls_repository = devices_controls_repository
        self.__devices_controls_manager = devices_controls_manager

        self.__channels_repository = channels_repository
        self.__channels_manager = channels_manager

        self.__channels_properties_repository = channels_properties_repository
        self.__channels_properties_manager = channels_properties_manager
        self.__channels_properties_states_repository = channels_properties_states_repository
        self.__channels_properties_states_manager = channels_properties_states_manager

        self.__channels_controls_repository = channels_controls_repository
        self.__channels_controls_manager = channels_controls_manager

        self.__event_dispatcher = event_dispatcher

        self.__logger = logger

    # -----------------------------------------------------------------------------

    def open(self) -> None:
        """Open all listeners callbacks"""
        self.__event_dispatcher.add_listener(
            event_id=DeviceRecordCreatedOrUpdatedEvent.EVENT_NAME,
            listener=self.__handle_update_device,
        )

        self.__event_dispatcher.add_listener(
            event_id=ChannelRecordCreatedOrUpdatedEvent.EVENT_NAME,
            listener=self.__handle_create_or_update_channel,
        )

        self.__event_dispatcher.add_listener(
            event_id=ChannelRecordDeletedEvent.EVENT_NAME,
            listener=self.__handle_delete_channel,
        )

        self.__event_dispatcher.add_listener(
            event_id=DevicePropertyRecordCreatedOrUpdatedEvent.EVENT_NAME,
            listener=self.__handle_create_or_update_device_property,
        )

        self.__event_dispatcher.add_listener(
            event_id=DevicePropertyRecordDeletedEvent.EVENT_NAME,
            listener=self.__handle_delete_device_property,
        )

        self.__event_dispatcher.add_listener(
            event_id=ChannelPropertyRecordCreatedOrUpdatedEvent.EVENT_NAME,
            listener=self.__handle_create_or_update_channel_property,
        )

        self.__event_dispatcher.add_listener(
            event_id=ChannelPropertyRecordDeletedEvent.EVENT_NAME,
            listener=self.__handle_delete_channel_property,
        )

        self.__event_dispatcher.add_listener(
            event_id=DevicePropertyActualValueEvent.EVENT_NAME,
            listener=self.__handle_write_device_property_actual_value,
        )

        self.__event_dispatcher.add_listener(
            event_id=ChannelPropertyActualValueEvent.EVENT_NAME,
            listener=self.__handle_write_channel_property_actual_value,
        )

        self.__event_dispatcher.add_listener(
            event_id=DeviceStateChangedEvent.EVENT_NAME,
            listener=self.__handle_write_device_state,
        )

    # -----------------------------------------------------------------------------

    def close(self) -> None:
        """Close all listeners registrations"""
        self.__event_dispatcher.remove_listener(
            event_id=DeviceRecordCreatedOrUpdatedEvent.EVENT_NAME,
            listener=self.__handle_update_device,
        )

        self.__event_dispatcher.remove_listener(
            event_id=ChannelRecordCreatedOrUpdatedEvent.EVENT_NAME,
            listener=self.__handle_create_or_update_channel,
        )

        self.__event_dispatcher.remove_listener(
            event_id=ChannelRecordDeletedEvent.EVENT_NAME,
            listener=self.__handle_delete_channel,
        )

        self.__event_dispatcher.remove_listener(
            event_id=DevicePropertyRecordCreatedOrUpdatedEvent.EVENT_NAME,
            listener=self.__handle_create_or_update_device_property,
        )

        self.__event_dispatcher.remove_listener(
            event_id=DevicePropertyRecordDeletedEvent.EVENT_NAME,
            listener=self.__handle_delete_device_property,
        )

        self.__event_dispatcher.remove_listener(
            event_id=ChannelPropertyRecordCreatedOrUpdatedEvent.EVENT_NAME,
            listener=self.__handle_create_or_update_channel_property,
        )

        self.__event_dispatcher.remove_listener(
            event_id=ChannelPropertyRecordDeletedEvent.EVENT_NAME,
            listener=self.__handle_delete_channel_property,
        )

        self.__event_dispatcher.remove_listener(
            event_id=DevicePropertyActualValueEvent.EVENT_NAME,
            listener=self.__handle_write_device_property_actual_value,
        )

        self.__event_dispatcher.remove_listener(
            event_id=ChannelPropertyActualValueEvent.EVENT_NAME,
            listener=self.__handle_write_channel_property_actual_value,
        )

        self.__event_dispatcher.remove_listener(
            event_id=DeviceStateChangedEvent.EVENT_NAME,
            listener=self.__handle_write_device_state,
        )

    # -----------------------------------------------------------------------------

    def __handle_update_device(self, event: Event) -> None:
        if not isinstance(event, DeviceRecordCreatedOrUpdatedEvent):
            return

        device = self.__devices_repository.get_by_id(device_id=event.record.id)

        if device is None:
            self.__logger.warning(
                "Device to updated was not found in database",
                extra={
                    "device": {
                        "id": event.record.id.__str__(),
                    },
                },
            )

            return

        device_data = {
            "id": event.record.id,
            "identifier": event.record.identifier,
            "name": event.record.name,
            "enabled": event.record.enabled,
            "hardware_manufacturer": event.record.hardware_manufacturer,
            "hardware_model": event.record.hardware_model,
            "hardware_version": event.record.hardware_version,
            "firmware_manufacturer": event.record.firmware_manufacturer,
            "firmware_version": event.record.firmware_version,
        }

        device = self.__devices_manager.update(data=device_data, device=device)

        self.__logger.debug(
            "Updating existing device",
            extra={
                "device": {
                    "id": device.id.__str__(),
                },
            },
        )

        self.__set_device_state(device=event.record)

        for existing_device_control in self.__devices_controls_repository.get_all_by_device(device_id=device.id):
            if existing_device_control.name not in event.record.controls:
                self.__devices_controls_manager.delete(device_control=existing_device_control)

                self.__logger.debug(
                    "Removing invalid device control",
                    extra={
                        "device": {
                            "id": device.id.__str__(),
                        },
                        "control": {
                            "name": existing_device_control.name,
                        },
                    },
                )

        for control_name in event.record.controls:
            device_control = self.__devices_controls_repository.get_by_name(
                device_id=device.id,
                control_name=control_name,
            )

            if device_control is None:
                device_control = self.__devices_controls_manager.create(
                    data={
                        "device_id": device.id,
                        "name": control_name,
                    }
                )

                self.__logger.debug(
                    "Creating new device control",
                    extra={
                        "device": {
                            "id": device_control.device.id.__str__(),
                        },
                        "control": {
                            "id": device_control.id.__str__(),
                            "name": device_control.name,
                        },
                    },
                )

    # -----------------------------------------------------------------------------

    def __handle_create_or_update_channel(self, event: Event) -> None:
        if not isinstance(event, ChannelRecordCreatedOrUpdatedEvent):
            return

        channel_data = {
            "id": event.record.id,
            "identifier": event.record.identifier,
            "name": event.record.name,
        }

        channel = self.__channels_repository.get_by_id(channel_id=event.record.id)

        if channel is None:
            # Define relation between channel and it's device
            channel_data["device_id"] = event.record.device_id

            channel = self.__channels_manager.create(data=channel_data)

            self.__logger.debug(
                "Creating new channel",
                extra={
                    "device": {
                        "id": channel.device.id.__str__(),
                    },
                    "channel": {
                        "id": channel.id.__str__(),
                    },
                },
            )

        else:
            channel = self.__channels_manager.update(data=channel_data, channel=channel)

            self.__logger.debug(
                "Updating existing channel",
                extra={
                    "device": {
                        "id": channel.device.id.__str__(),
                    },
                    "channel": {
                        "id": channel.id.__str__(),
                    },
                },
            )

        for existing_channel_control in self.__channels_controls_repository.get_all_by_channel(channel_id=channel.id):
            if existing_channel_control.name not in event.record.controls:
                self.__channels_controls_manager.delete(channel_control=existing_channel_control)

                self.__logger.debug(
                    "Removing invalid channel control",
                    extra={
                        "device": {
                            "id": channel.device.id.__str__(),
                        },
                        "channel": {
                            "id": channel.id.__str__(),
                        },
                        "control": {
                            "name": existing_channel_control.name,
                        },
                    },
                )

        for control_name in event.record.controls:
            channel_control = self.__channels_controls_repository.get_by_name(
                channel_id=channel.id,
                control_name=control_name,
            )

            if channel_control is None:
                channel_control = self.__channels_controls_manager.create(
                    data={
                        "channel_id": channel.id,
                        "name": control_name,
                    }
                )

                self.__logger.debug(
                    "Creating new device control",
                    extra={
                        "device": {
                            "id": channel_control.channel.device.id.__str__(),
                        },
                        "channel": {
                            "id": channel_control.channel.id.__str__(),
                        },
                        "control": {
                            "id": channel_control.id.__str__(),
                            "name": channel_control.name,
                        },
                    },
                )

    # -----------------------------------------------------------------------------

    def __handle_delete_channel(self, event: Event) -> None:
        if not isinstance(event, ChannelRecordDeletedEvent):
            return

        channel = self.__channels_repository.get_by_id(channel_id=event.record.id)

        if channel is not None:
            self.__channels_manager.delete(channel=channel)

            self.__logger.debug(
                "Removing existing device property",
                extra={
                    "device": {
                        "id": channel.device.id.__str__(),
                    },
                    "channel": {
                        "id": channel.id.__str__(),
                    },
                },
            )

    # -----------------------------------------------------------------------------

    def __handle_create_or_update_device_property(self, event: Event) -> None:
        if not isinstance(event, DevicePropertyRecordCreatedOrUpdatedEvent):
            return

        property_data = {
            "id": event.record.id,
            "identifier": event.record.identifier,
            "name": event.record.name,
            "data_type": event.record.data_type,
            "format": event.record.format,
            "unit": event.record.unit,
            "invalid": None,
            "queryable": event.record.queryable,
            "settable": event.record.settable,
        }

        device_property = self.__devices_properties_repository.get_by_id(property_id=event.record.id)

        if device_property is None:
            # Define relation between channel and it's device
            property_data["device_id"] = event.record.device_id

            device_property = self.__devices_properties_manager.create(
                data=property_data,
                property_type=ChannelDynamicPropertyEntity,
            )

            self.__logger.debug(
                "Creating new device property",
                extra={
                    "device": {
                        "id": device_property.device.id.__str__(),
                    },
                    "property": {
                        "id": device_property.id.__str__(),
                    },
                },
            )

        else:
            device_property = self.__devices_properties_manager.update(
                data=device_property,
                device_property=device_property,
            )

            self.__logger.debug(
                "Updating existing device property",
                extra={
                    "device": {
                        "id": device_property.device.id.__str__(),
                    },
                    "property": {
                        "id": device_property.id.__str__(),
                    },
                },
            )

    # -----------------------------------------------------------------------------

    def __handle_delete_device_property(self, event: Event) -> None:
        if not isinstance(event, DevicePropertyRecordDeletedEvent):
            return

        device_property = self.__devices_properties_repository.get_by_id(property_id=event.record.id)

        if device_property is not None:
            self.__devices_properties_manager.delete(device_property=device_property)

            self.__logger.debug(
                "Removing existing device property",
                extra={
                    "device": {
                        "id": device_property.device.id.__str__(),
                    },
                    "property": {
                        "id": device_property.id.__str__(),
                    },
                },
            )

    # -----------------------------------------------------------------------------

    def __handle_create_or_update_channel_property(self, event: Event) -> None:
        if not isinstance(event, ChannelPropertyRecordCreatedOrUpdatedEvent):
            return

        property_data = {
            "id": event.record.id,
            "identifier": event.record.identifier,
            "name": event.record.name,
            "data_type": event.record.data_type,
            "format": event.record.format,
            "unit": event.record.unit,
            "invalid": None,
            "queryable": event.record.queryable,
            "settable": event.record.settable,
        }

        channel_property = self.__channels_properties_repository.get_by_id(property_id=event.record.id)

        if channel_property is None:
            # Define relation between channel and it's channel
            property_data["channel_id"] = event.record.channel_id

            channel_property = self.__channels_properties_manager.create(
                data=property_data,
                property_type=DeviceDynamicPropertyEntity,
            )

            self.__logger.debug(
                "Creating new channel property",
                extra={
                    "device": {
                        "id": channel_property.channel.device.id.__str__(),
                    },
                    "channel": {
                        "id": channel_property.channel.id.__str__(),
                    },
                    "property": {
                        "id": channel_property.id.__str__(),
                    },
                },
            )

        else:
            channel_property = self.__channels_properties_manager.update(
                data=channel_property,
                channel_property=channel_property,
            )

            self.__logger.debug(
                "Updating existing channel property",
                extra={
                    "device": {
                        "id": channel_property.channel.device.id.__str__(),
                    },
                    "channel": {
                        "id": channel_property.channel.id.__str__(),
                    },
                    "property": {
                        "id": channel_property.id.__str__(),
                    },
                },
            )

    # -----------------------------------------------------------------------------

    def __handle_delete_channel_property(self, event: Event) -> None:
        if not isinstance(event, ChannelPropertyRecordDeletedEvent):
            return

        channel_property = self.__channels_properties_repository.get_by_id(property_id=event.record.id)

        if channel_property is not None:
            self.__channels_properties_manager.delete(channel_property=channel_property)

            self.__logger.debug(
                "Removing existing channel property",
                extra={
                    "device": {
                        "id": channel_property.channel.device.id.__str__(),
                    },
                    "channel": {
                        "id": channel_property.channel.id.__str__(),
                    },
                    "property": {
                        "id": channel_property.id.__str__(),
                    },
                },
            )

    # -----------------------------------------------------------------------------

    def __handle_write_device_property_actual_value(self, event: Event) -> None:
        if not isinstance(event, DevicePropertyActualValueEvent):
            return

        if self.__devices_properties_states_repository is None or self.__devices_properties_states_manager is None:
            return

        device_property = self.__devices_properties_repository.get_by_id(property_id=event.updated_record.id)

        if device_property is not None:
            state_data = {
                "actual_value": event.updated_record.actual_value,
            }

            property_state = self.__devices_properties_states_repository.get_by_id(property_id=device_property.id)

            if property_state is None:
                property_state = self.__devices_properties_states_manager.create(
                    device_property=device_property,
                    data=state_data,
                )

                self.__logger.debug(
                    "Creating new channel property state",
                    extra={
                        "device": {
                            "id": device_property.device.id.__str__(),
                        },
                        "property": {
                            "id": device_property.id.__str__(),
                        },
                        "state": {
                            "id": property_state.id.__str__(),
                            "actual_value": property_state.actual_value,
                            "expected_value": property_state.expected_value,
                            "pending": property_state.pending,
                        },
                    },
                )

            else:
                property_state = self.__devices_properties_states_manager.update(
                    device_property=device_property,
                    state=property_state,
                    data=state_data,
                )

                self.__logger.debug(
                    "Updating existing channel property state",
                    extra={
                        "device": {
                            "id": device_property.device.id.__str__(),
                        },
                        "property": {
                            "id": device_property.id.__str__(),
                        },
                        "state": {
                            "id": property_state.id.__str__(),
                            "actual_value": property_state.actual_value,
                            "expected_value": property_state.expected_value,
                            "pending": property_state.pending,
                        },
                    },
                )

    # -----------------------------------------------------------------------------

    def __handle_write_channel_property_actual_value(self, event: Event) -> None:
        if not isinstance(event, ChannelPropertyActualValueEvent):
            return

        if self.__channels_properties_states_repository is None or self.__channels_properties_states_manager is None:
            return

        channel_property = self.__channels_properties_repository.get_by_id(property_id=event.updated_record.id)

        if channel_property is not None:
            state_data = {
                "actual_value": event.updated_record.actual_value,
            }

            property_state = self.__channels_properties_states_repository.get_by_id(property_id=channel_property.id)

            if property_state is None:
                property_state = self.__channels_properties_states_manager.create(
                    channel_property=channel_property,
                    data=state_data,
                )

                self.__logger.debug(
                    "Creating new channel property state",
                    extra={
                        "device": {
                            "id": channel_property.channel.device.id.__str__(),
                        },
                        "channel": {
                            "id": channel_property.channel.id.__str__(),
                        },
                        "property": {
                            "id": channel_property.id.__str__(),
                        },
                        "state": {
                            "id": property_state.id.__str__(),
                            "actual_value": property_state.actual_value,
                            "expected_value": property_state.expected_value,
                            "pending": property_state.pending,
                        },
                    },
                )

            else:
                property_state = self.__channels_properties_states_manager.update(
                    channel_property=channel_property,
                    state=property_state,
                    data=state_data,
                )

                self.__logger.debug(
                    "Updating existing channel property state",
                    extra={
                        "device": {
                            "id": channel_property.channel.device.id.__str__(),
                        },
                        "channel": {
                            "id": channel_property.channel.id.__str__(),
                        },
                        "property": {
                            "id": channel_property.id.__str__(),
                        },
                        "state": {
                            "id": property_state.id.__str__(),
                            "actual_value": property_state.actual_value,
                            "expected_value": property_state.expected_value,
                            "pending": property_state.pending,
                        },
                    },
                )

    # -----------------------------------------------------------------------------

    def __handle_write_device_state(self, event: Event) -> None:
        if not isinstance(event, DeviceStateChangedEvent):
            return

        self.__set_device_state(device=event.record)

    # -----------------------------------------------------------------------------

    def __set_device_state(self, device: DeviceRecord) -> None:
        state_property = self.__devices_properties_repository.get_by_identifier(
            device_id=device.id,
            property_identifier=DevicePropertyName.STATE.value,
        )

        if state_property is None:
            property_data = {
                "identifier": DevicePropertyName.STATE.value,
                "data_type": DataType.ENUM,
                "format": [
                    ConnectionState.CONNECTED.value,
                    ConnectionState.DISCONNECTED.value,
                    ConnectionState.INIT.value,
                    ConnectionState.READY.value,
                    ConnectionState.RUNNING.value,
                    ConnectionState.SLEEPING.value,
                    ConnectionState.STOPPED.value,
                    ConnectionState.LOST.value,
                    ConnectionState.ALERT.value,
                    ConnectionState.UNKNOWN.value,
                ],
                "unit": None,
                "invalid": None,
                "queryable": False,
                "settable": False,
                "value": device.state.value,
            }

            state_property = self.__devices_properties_manager.create(
                data=property_data,
                property_type=DeviceStaticPropertyEntity,
            )

            self.__logger.debug(
                "Creating device state property",
                extra={
                    "device": {
                        "id": device.id.__str__(),
                    },
                    "property": {
                        "id": state_property.id.__str__(),
                    },
                },
            )

        else:
            property_data = {"value": device.state.value}

            state_property = self.__devices_properties_manager.update(
                data=property_data,
                device_property=state_property,
            )

            self.__logger.debug(
                "Updating device state property",
                extra={
                    "device": {
                        "id": device.id.__str__(),
                    },
                    "property": {
                        "id": state_property.id.__str__(),
                    },
                },
            )
