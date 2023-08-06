# Introduction 
The my-pv-lib Python package provides easy useage of products from my-pv GmbH in python projects.

# Installation
`pip install my-pv-lib`

# Usage
The Python package basicaly provides the following functionalities:
- Device implementations for access device data and settings in own projects like for example home automation solutions.
- Connecting Devices to Cloud Services
- Additional Tools

## Devices
A device will handle connections to a real device and provides access to settings and data in an easy to use way.
All devices provide acces to data via so called channels. Which channels are provided is depending on the specific device and it's functionalities an is descriped in the device description. Channels can be read-only, write-only or read-and-write depending on the devices capabilities. Using a channel in a wrong direction will cause an exception.

### Power Meter
#### Channels
- power: power measured in W

#### Constructor
Powermeter(Serialnumber, [Hostname or IP Address of the device])`

#### Examples
Getting latest power value by reading the power channel
``` 
device = Powermeter("1530638", None)
device.readallregisters()
power = device.getchannelvalue("power")
print("Channel power: " + str(power))
```


# Contribute
Please report bug, feature requests or your own code to info@my-pv.com 