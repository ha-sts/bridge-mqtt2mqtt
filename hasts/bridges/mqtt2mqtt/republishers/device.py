#!/usr/bin/env python3

### IMPORTS ###
import logging

### GLOBALS ###

### FUNCTIONS ###

### CLASSES ###
class Device:
    def __init__(self, device_id):
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.debug("Inputs - device_id: %s", device_id)
        self.device_id = device_id

    async def handle_message(self, message):
        raise NotImplementedError

class DeviceManager:
    def __init__(self, mqtt_client):
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.debug("Inputs - mqtt_client: %s", mqtt_client)
        self._mqtt_client = mqtt_client
        self.devices = {}
        self.prefix = "generic"

    async def _handle_message(self, message):
        raise NotImplementedError

    async def register_coroutines(self):
        # This should be called after the creation of this class to enable listening for messages.
        await self._mqtt_client.register_topic_coroutine("{}/#".format(self._prefix), self._handle_message)
