#!/bin/bash

# Simple script to run the lap timer application on RP2040

DEVICE="/dev/tty.usbmodem1101"

# Check if device exists
if [ ! -e "$DEVICE" ]; then
    echo "Device not found at $DEVICE"
    echo "Searching for USB devices..."
    ls /dev/tty.usb* /dev/cu.usb* 2>/dev/null || echo "No USB devices found"
    exit 1
fi

echo "Running lap timer on $DEVICE..."
mpremote connect "$DEVICE" run main.py
