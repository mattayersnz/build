# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a MicroPython lap timer application for the Adafruit RP2040 (Feather) with an SH1107 OLED display. The project runs directly on the microcontroller hardware, not on a desktop OS.

## Hardware Configuration

**Components**:
- Adafruit Feather RP2040 with USB Type A Host
- Adafruit FeatherWing OLED - 128x64 OLED Add-on for Feather (STEMMA QT / Qwiic)
- Solderable protoboard (EPLZON breadboard-compatible)

**Protoboard Wiring**:

*RP2040 to OLED connections:*
- 3V → 3V
- GND → GND
- SDA → SDA (GPIO 2 on RP2040)
- SCL → SCL (GPIO 3 on RP2040)

*Button connections to RP2040:*
- GPIO 9 → Button A (Start/Stop/Reset with long-press)

**Pin Assignments**:
- I2C SCL: GPIO 3
- I2C SDA: GPIO 2
- I2C Address: 0x3c (SH1107 OLED 128x64)
- Button A (Start/Stop/Reset): GPIO 9
- Button is active LOW with internal pull-up resistor
- Display rotation: 180° (upside-down corrected)

## Development Commands

### Quick Deploy (Recommended)

Use the deploy script to upload files and run the app on boot:

```bash
./deploy.sh
```

Or use the local alias when in the project directory (after running `source .envrc` or installing direnv):

```bash
build
```

### Device Connection
All commands use mpremote to communicate with the RP2040. The device path is typically `/dev/tty.usbmodem1101` on macOS. If the device is not found:

```bash
ls /dev/tty.usb* /dev/cu.usb*
```

### Manual Upload Files to Device
```bash
# Upload SH1107 driver library
mpremote connect /dev/tty.usbmodem1101 fs cp sh1107.py :

# Upload main application
mpremote connect /dev/tty.usbmodem1101 fs cp main.py :
```

### Run Application
```bash
# Quick deploy (recommended) - auto-runs on boot
./deploy.sh

# Run once (stops when terminal closes)
./run.sh
# or manually:
mpremote connect /dev/tty.usbmodem1101 run main.py

# Copy as boot.py for auto-start on power-on
mpremote connect /dev/tty.usbmodem1101 fs cp main.py :boot.py

# Soft reset if main.py already on device
mpremote connect /dev/tty.usbmodem1101 soft-reset
```

### Testing
```bash
# Test I2C device detection
mpremote connect /dev/tty.usbmodem1101 run test_01_hardware.py

# Test display output
mpremote connect /dev/tty.usbmodem1101 run test_sh1107_display.py
```

### REPL Access
```bash
# Enter interactive REPL
mpremote connect /dev/tty.usbmodem1101 repl

# Press Ctrl+] to exit REPL
```

## Architecture

**main.py**: Core application implementing the timer state machine
- Manages timer state (running, start_time, elapsed)
- Single-button control with long-press detection (1 second threshold)
- Short press: Start/Stop toggle with pause/resume capability
- Long press: Reset timer to 00:00.000
- Display updates using format_time() helper (MM:SS.thm format - minutes:seconds.tenths-hundredths-milliseconds)
- Main loop: polls button at 50ms intervals, updates display when running
- Display rotation set to 180° for correct orientation
- Auto-runs on boot for standalone operation

**sh1107.py**: SH1107 OLED driver library (from peter-l5/SH1107)
- SH1107_I2C class for I2C communication
- SH1107_SPI class for SPI communication (not used in this project)
- Subclasses framebuf.FrameBuffer for graphics primitives
- Handles low-level display initialization and command sequences
- Optimized for SH1107 controller (used in Adafruit FeatherWing OLED 128x64)

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
