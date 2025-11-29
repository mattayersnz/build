# Lap Timer for Adafruit RP2040

A MicroPython-based lap timer application for the Adafruit RP2040 with an SSD1306 OLED display.

## Hardware Requirements

- Adafruit RP2040 (Feather or compatible board)
- SSD1306 OLED Display (128x64, I2C)
- 3 Push buttons
- MicroPython firmware installed on the RP2040

## Pin Configuration

### I2C Connection (OLED Display)
- **SCL**: GPIO 3
- **SDA**: GPIO 2
- **I2C Address**: 0x3c

### Buttons (Active LOW with pull-up resistors)
- **Button A** (Start): GPIO 5
- **Button B** (Stop): GPIO 6
- **Button C** (Reset): GPIO 9

## Features

- Start/Stop/Reset timer functionality
- Display shows time in MM:SS.hh format
- Real-time status indicator (RUNNING/STOPPED)
- Edge-detection debouncing for reliable button input

## Installation

### Prerequisites

Install mpremote for device communication:

```bash
brew install mpremote
```

### Upload Files to RP2040

1. Connect your RP2040 via USB

2. Upload the SSD1306 driver library:
```bash
mpremote connect /dev/tty.usbmodem101 fs cp ssd1306.py :
```

3. Upload the main application:
```bash
mpremote connect /dev/tty.usbmodem101 fs cp main.py :
```

## Running the Application

### Option 1: Run Once (Temporary)

Run the app directly - it will stop when you close the terminal or disconnect:

```bash
mpremote connect /dev/tty.usbmodem101 run main.py
```

### Option 2: Auto-Run on Boot (Recommended)

Make the app start automatically when the RP2040 powers on:

```bash
mpremote connect /dev/tty.usbmodem101 fs cp main.py :boot.py
```

After this, simply disconnect and reconnect power - the lap timer will start automatically.

### Option 3: Via REPL

Connect to the REPL and import the module:

```bash
mpremote connect /dev/tty.usbmodem101 repl
```

Then in the REPL:
```python
import main
```

Press `Ctrl+]` to exit the REPL.

### Option 4: Soft Reset

If `main.py` is already on the device:

```bash
mpremote connect /dev/tty.usbmodem101 soft-reset
```

## Usage

Once running, the OLED display will show:

```
LAP TIMER
00:00.00
STOPPED
```

### Button Controls

- **Button A**: Start the timer
- **Button B**: Stop/Pause the timer
- **Button C**: Reset the timer to 00:00.00

## Troubleshooting

### Display shows pixel noise

The app includes automatic display reset on startup. If you still see noise:

1. Power cycle the RP2040
2. Re-upload the files
3. Check I2C connections

### Buttons not responding

1. Verify GPIO pin numbers match your hardware
2. Check that buttons are wired as active LOW with pull-up resistors
3. Ensure buttons are properly connected to ground when pressed

### Device not found

Check your USB connection and find the correct device:

```bash
ls /dev/tty.usb* /dev/cu.usb*
```

Replace `/dev/tty.usbmodem101` in the commands with your actual device path.

## File Structure

- `main.py` - Main application code
- `ssd1306.py` - SSD1306 OLED driver library
- `README.md` - This file

## License

Open source - feel free to modify and adapt for your needs.
