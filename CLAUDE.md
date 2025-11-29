# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a MicroPython lap timer application for the Adafruit RP2040 (Feather) with an SSD1306 OLED display. The project runs directly on the microcontroller hardware, not on a desktop OS.

## Hardware Configuration

**Target Device**: Adafruit RP2040 Feather board with MicroPython firmware

**Pin Assignments**:
- I2C SCL: GPIO 3
- I2C SDA: GPIO 2
- I2C Address: 0x3c (SSD1306 OLED 128x64)
- Button A (Start): GPIO 5
- Button B (Stop): GPIO 6
- Button C (Reset): GPIO 9
- All buttons are active LOW with internal pull-up resistors

## Development Commands

### Device Connection
All commands use mpremote to communicate with the RP2040. The device path is typically `/dev/tty.usbmodem101` on macOS. If the device is not found:

```bash
ls /dev/tty.usb* /dev/cu.usb*
```

### Upload Files to Device
```bash
# Upload SSD1306 driver library
mpremote connect /dev/tty.usbmodem101 fs cp ssd1306.py :

# Upload main application
mpremote connect /dev/tty.usbmodem101 fs cp main.py :
```

### Run Application
```bash
# Run once (stops when terminal closes)
mpremote connect /dev/tty.usbmodem101 run main.py

# Copy as boot.py for auto-start on power-on
mpremote connect /dev/tty.usbmodem101 fs cp main.py :boot.py

# Soft reset if main.py already on device
mpremote connect /dev/tty.usbmodem101 soft-reset
```

### Testing
```bash
# Test I2C device detection
mpremote connect /dev/tty.usbmodem101 run test_i2c.py

# Test display output
mpremote connect /dev/tty.usbmodem101 run test_display.py
```

### REPL Access
```bash
# Enter interactive REPL
mpremote connect /dev/tty.usbmodem101 repl

# Press Ctrl+] to exit REPL
```

## Architecture

**main.py**: Core application implementing the timer state machine
- Manages timer state (running, start_time, elapsed)
- Edge-detection button debouncing (tracks last button state)
- Display updates using format_time() helper (MM:SS.hh format)
- Main loop: polls buttons at 50ms intervals, updates display when running

**ssd1306.py**: SSD1306 OLED driver library (standard MicroPython driver)
- SSD1306_I2C class for I2C communication
- SSD1306_SPI class for SPI communication (not used in this project)
- Subclasses framebuf.FrameBuffer for graphics primitives
- Handles low-level display initialization and command sequences

**test_i2c.py**: Hardware diagnostic script
- Scans multiple I2C bus configurations
- Helps identify correct GPIO pins and I2C addresses

**test_display.py**: Display verification script
- Simple "Hello" test for confirming OLED is working
- Uses same I2C configuration as main application

## Display Initialization Pattern

The display requires a specific power-cycle sequence to avoid pixel noise:

```python
oled.poweroff()
time.sleep(0.1)
oled.fill(0)
oled.poweron()
oled.show()
```

This pattern is implemented in main.py:10-19 and should be preserved when modifying display initialization code.

## Button Debouncing Implementation

The application uses edge-detection debouncing by tracking previous button states:

```python
btnA_current = btnA.value()
if btnA_last and not btnA_current:  # falling edge detection
    # handle button press
btnA_last = btnA_current
```

This pattern detects the transition from HIGH to LOW (button press) and is critical for reliable button input. Modify with caution.

## MicroPython Constraints

- This code runs on a microcontroller, not CPython
- No access to standard library modules beyond micropython, machine, framebuf, and time
- Memory-constrained environment (avoid large allocations)
- Use time.ticks_ms() for millisecond timing, not time.time()
- No file I/O on the device filesystem during normal operation
- All code must be compatible with MicroPython syntax and available modules
