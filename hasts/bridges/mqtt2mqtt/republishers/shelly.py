#!/usr/bin/env python3

### IMPORTS ###
import logging

from device import Device, DeviceManager

### GLOBALS ###

### FUNCTIONS ###

### CLASSES ###
class ShellyDevice(Device):
    def __init__(self, device_id):
        super().__init__(device_id)

    async def handle_message(self, message):
        self.logger.debug("message: %s", message)
        tmp_topic_split = message.topic.value().split('/')
        tmp_payload = message.payload.decode('utf-8')
        # shelly topic formats (input):
        #  - switch: shelly/<device_id>/status/switch:<unit_number> (contains energy and temperature also)
        # ha-sts topic formats (output):
        #  - switch: hasts/switch/<device_id>/<unit_number>/state
        #  - energy: hasts/energy/<device_id>/<unit_number>/current_voltage
        #            hasts/energy/<device_id>/<unit_number>/current_amperage
        #            hasts/energy/<device_id>/<unit_number>/current_power
        #            hasts/energy/<device_id>/<unit_number>/current_powerfactor
        #            hasts/energy/<device_id>/<unit_number>/current_frequency
        #            hasts/energy/<device_id>/<unit_number>/cumulative_energy
        #  - temperature: hasts/temperature/<device_id>/<unit_number>/temp_c
        #                 hasts/temperature/<device_id>/<unit_number>/temp_f
        # Verify the device_id for good measure
        if tmp_topic_split[1] != self.device_id:
            self.logger.warn("message device_id %s doesn't match %s", tmp_topic_split[1], self.device_id)
            return # Just fail out if the device_ids don't match


class ShellyDeviceManager(DeviceManager):
    def __init__(self, mqtt_client):
        super().__init__(mqtt_client)
        self.prefix = "shelly"

    async def _handle_message(self, message):
        self.logger.debug("Received message: %s", message)
        tmp_topic = message.topic.value()
        #tmp_payload = message.payload.decode('utf-8')
        # Check to see if the device has been seen before
        #    - if not, create a new device
        # shelly topic format: shelly/<device_id>/status/<unit>
        tmp_topic_split = tmp_topic.split('/')
        tmp_device_id = str(tmp_topic_split[1])
        if tmp_device_id not in self.devices:
            self.devices[tmp_device_id] = ShellyDevice(tmp_device_id)
        # Forward the message to the device
        self.devices[tmp_device_id].handle_message(message)
