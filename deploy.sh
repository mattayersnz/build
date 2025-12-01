#!/bin/bash

# Deploy lap timer application to RP2040 (runs on boot)

DEVICE="/dev/tty.usbmodem1101"

# Check if device exists
if [ ! -e "$DEVICE" ]; then
    echo "Device not found at $DEVICE"
    echo "Searching for USB devices..."
    ls /dev/tty.usb* /dev/cu.usb* 2>/dev/null || echo "No USB devices found"
    exit 1
fi

echo "Stopping any running programs..."
# Try to interrupt running program with Ctrl+C
printf "\x03" > "$DEVICE" 2>/dev/null || true
sleep 0.5

echo "Uploading ssd1306.py to $DEVICE..."
mpremote connect "$DEVICE" fs cp ssd1306.py :

echo "Uploading main.py as boot.py to $DEVICE..."
mpremote connect "$DEVICE" fs cp main.py :boot.py

echo "Soft resetting device to start application..."
if mpremote connect "$DEVICE" soft-reset 2>/dev/null; then
    echo "Done! Application is now running and will auto-start on power-up."
else
    echo "Soft reset failed (device may be busy)."
    echo "To start the app, unplug and replug the USB cable."
    echo "The app will auto-start on power-up."
fi
