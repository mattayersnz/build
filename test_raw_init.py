# test_raw_init.py
# Raw SSD1306 initialization based on Adafruit specs

from machine import Pin, I2C
import time

print("=" * 40)
print("Raw Initialization Test")
print("=" * 40)

i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
addr = 0x3c

def write_cmd(cmd):
    """Write command to display"""
    i2c.writeto(addr, bytes([0x00, cmd]))

def write_data(data):
    """Write data to display"""
    i2c.writeto(addr, bytes([0x40] + list(data)))

print("Initializing display with Adafruit FeatherWing sequence...")

# Display OFF
write_cmd(0xAE)

# Set display clock divide ratio/oscillator frequency
write_cmd(0xD5)
write_cmd(0x80)

# Set multiplex ratio (height - 1)
write_cmd(0xA8)
write_cmd(0x3F)  # 63 for 64 rows

# Set display offset
write_cmd(0xD3)
write_cmd(0x00)

# Set display start line
write_cmd(0x40 | 0x00)

# Set charge pump
write_cmd(0x8D)
write_cmd(0x14)  # Enable charge pump

# Set memory addressing mode (horizontal)
write_cmd(0x20)
write_cmd(0x00)

# Set segment remap (flip horizontally)
write_cmd(0xA0 | 0x01)

# Set COM output scan direction
write_cmd(0xC0 | 0x08)

# Set COM pins hardware configuration
write_cmd(0xDA)
write_cmd(0x12)  # Alternative COM pin, no remap

# Set contrast
write_cmd(0x81)
write_cmd(0xCF)  # Adafruit default contrast

# Set precharge period
write_cmd(0xD9)
write_cmd(0xF1)

# Set VCOMH deselect level
write_cmd(0xDB)
write_cmd(0x40)

# Entire display ON (resume from RAM)
write_cmd(0xA4)

# Set normal display (not inverted)
write_cmd(0xA6)

# Display ON
write_cmd(0xAF)

print("Display initialized!")

# Clear display
print("Clearing display...")
# Set column address range
write_cmd(0x21)
write_cmd(0)
write_cmd(127)

# Set page address range
write_cmd(0x22)
write_cmd(0)
write_cmd(7)

# Write zeros to clear
for _ in range(128 * 8):
    write_data([0])

time.sleep(1)

# Fill display with white
print("Filling with white...")
write_cmd(0x21)
write_cmd(0)
write_cmd(127)
write_cmd(0x22)
write_cmd(0)
write_cmd(7)

for _ in range(128 * 8):
    write_data([0xFF])

print("\n" + "=" * 40)
print("Display should be completely white")
print("Is it clean? Or still noisy?")
print("=" * 40)
