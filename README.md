# bridge-mqtt2mqtt
MQTT republisher to change the format of MQTT messages.

The first items that will be republished are the Shelly plugs and switches.  They publish in a format that is much more
complicated than the basic format used by HA-STS.  The Shelly units will be expected to be configured with the MQTT
prefix being `shelly/<device_id>` with the device_id formatted as an ethernet MAC address (e.g. `11:22:33:44:55:66`).

The next items that will be republished are the OpenGarage modules.

The HA-STS MQTT topic structure is as follows:
```
<device_id> - MAC address format (e.g. '11:33:55:77:99:AA')
<unit_id> - unsigned integer specified by the device, or starting at 0 if none supplied 

hasts/
    switch/
        <device_id>/
            <unit_id>/
                state   - current state of the switch ('on' or 'off')
                change_state   - the state to set the switch ('on' or 'off')
    energy/
        <device_id>/
            <unit_id>/
                current_voltage   - decimal number for voltage
                current_amperage   - decimal number for amperage
                current_power   - decimal number for wattage
                current_powerfactor - decimal number for power factor
                current_frequency - decimal number for frequency
                cumulative_energy   - decimal number for watt-hours
    temperature/
        <device_id>/
            <unit_id>/
                temp_c   - decimal number for temperature in Celcius
                temp_f   - decimal number for temperature in Fahrenheit
    garage_door/
        <device_id>/
            <unit_id>/
                state   - current state of the door ('open' or 'closed')
                change_state   - the state to set the door ('open' or 'close')
                car_inside   - boolean string ('true' or 'false') stating whether the car is in the garage
```
