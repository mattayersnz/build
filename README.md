# Lap Timer for Adafruit RP2040

A MicroPython-based lap timer application for the Adafruit RP2040 with an SH1107 OLED display.

## Quick Start

### Prerequisites

Install mpremote for device communication:

```bash
brew install mpremote
```

### Deploy to Device

1. Connect your RP2040 via USB

2. Run the deploy script:
```bash
./deploy.sh
```

That's it! The lap timer will start automatically and continue running even after you disconnect the terminal.

**Local Shortcut**: When in this project directory, you can also type:
```bash
build
```

To activate the shortcut:
```bash
# Option 1: Using direnv (auto-loads when entering directory)
brew install direnv
direnv allow

# Option 2: Manual (load each time)
source .envrc
```

## Hardware Requirements

- Adafruit Feather RP2040 with USB Type A Host
- Adafruit FeatherWing OLED - 128x64 OLED Add-on for Feather (STEMMA QT / Qwiic)
- Solderable protoboard for mounting components
- MicroPython firmware installed on the RP2040

## Wiring on Protoboard

### RP2040 to OLED Display
- **3V** → **3V**
- **GND** → **GND**
- **SDA** → **SDA** (GPIO 2 on RP2040)
- **SCL** → **SCL** (GPIO 3 on RP2040)
- **I2C Address**: 0x3c

### Button Connections to RP2040
- **GPIO 9** → **Button A** (Start/Stop/Reset with long-press)
- Button is active LOW with internal pull-up resistor enabled

## Features

- Single-button control with short-press and long-press detection
- High-precision time display in SS.thm format (e.g., 12.567 seconds)
- Real-time status indicator (RUNNING/STOPPED)
- Pause/resume capability - preserves elapsed time
- Long-press reset (hold 1 second to reset timer)
- Edge-detection debouncing for reliable button input
- 180° display rotation for correct orientation
- Auto-run on boot - works standalone when powered

## Usage

Once running, the OLED display will show:

```
LAP TIMER
00:0.0.0
STOPPED
```

The time format shows seconds.tenths-hundredths-milliseconds (e.g., 12.567 = 12.567 seconds)

### Button Controls

**Button A (GPIO 9) - Single Button Control:**
- **Short press (tap)**: Start/Stop toggle
  - Tap to start timer
  - Tap again to pause (preserves elapsed time)
  - Tap again to resume from where paused
- **Long press (hold 1 second)**: Reset timer to 00.000
  - Timer resets immediately when held for 1 second

## Troubleshooting

### Display shows pixel noise or wrong controller

This project uses the **SH1107 OLED controller** (not SSD1306). The Adafruit FeatherWing OLED 128x64 uses SH1107.

If you see pixel noise:
1. Ensure you're using sh1107.py driver (not ssd1306.py)
2. Verify I2C address is 0x3c
3. Power cycle the RP2040
4. Check I2C connections

### Buttons not responding

1. Verify GPIO pin numbers match your hardware
2. Check that buttons are wired as active LOW with pull-up resistors
3. Ensure buttons are properly connected to ground when pressed

### Device not found

Check your USB connection and find the correct device:

```bash
ls /dev/tty.usb* /dev/cu.usb*
```

Replace `/dev/tty.usbmodem1101` in the commands with your actual device path.

## Manual Deployment (Advanced)

If you need more control, you can manually upload files:

```bash
# Upload SH1107 driver library
mpremote connect /dev/tty.usbmodem1101 fs cp sh1107.py :

# Upload main application
mpremote connect /dev/tty.usbmodem1101 fs cp main.py :

# Soft reset device (auto-runs main.py on boot)
mpremote connect /dev/tty.usbmodem1101 soft-reset
```

### Other Run Options

**Run once (temporary)** - stops when terminal closes:
```bash
./run.sh
```

**Via REPL**:
```bash
mpremote connect /dev/tty.usbmodem1101 repl
```

## File Structure

- `main.py` - Main application code with lap timer logic
- `sh1107.py` - SH1107 OLED driver library (from peter-l5/SH1107)
- `deploy.sh` - Deployment script (uploads and runs on boot)
- `run.sh` - Run script (temporary, stops on disconnect)
- `.envrc` - Local environment aliases
- `test_sh1107_display.py` - Display verification test
- `test_01_hardware.py` - I2C and hardware detection test

## License

Open source - feel free to modify and adapt for your needs.
