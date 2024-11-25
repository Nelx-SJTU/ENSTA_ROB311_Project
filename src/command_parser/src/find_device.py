#!/usr/bin/env python
import pyaudio

# Initialize PyAudio
p = pyaudio.PyAudio()

# List all audio devices
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    print("Device {}: {} (Input Channels: {})".format(i, device_info['name'], device_info['maxInputChannels']))


p.terminate()
