# test_pattern.py
# Draw specific patterns to diagnose the issue

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

print("=" * 40)
print("Pattern Diagnostic Test")
print("=" * 40)

i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

# Test 1: Horizontal stripes
print("\nTest 1: Drawing horizontal stripes...")
oled.fill(0)
for y in range(0, 64, 4):
    for x in range(128):
        oled.pixel(x, y, 1)
        oled.pixel(x, y+1, 1)
oled.show()
print("You should see horizontal white stripes")
print("Top half (blank area): See any stripes?")
print("Bottom half (noise area): See any stripes?")
time.sleep(3)

# Test 2: Top half only
print("\nTest 2: Drawing ONLY in top half (rows 0-31)...")
oled.fill(0)
for y in range(32):
    for x in range(128):
        oled.pixel(x, y, 1)
oled.show()
print("Top half should be white, bottom should be black")
time.sleep(3)

# Test 3: Bottom half only
print("\nTest 3: Drawing ONLY in bottom half (rows 32-63)...")
oled.fill(0)
for y in range(32, 64):
    for x in range(128):
        oled.pixel(x, y, 1)
oled.show()
print("Top half should be black, bottom should be white")
time.sleep(3)

# Test 4: Checkerboard
print("\nTest 4: Checkerboard pattern...")
oled.fill(0)
for y in range(64):
    for x in range(128):
        if (x + y) % 2 == 0:
            oled.pixel(x, y, 1)
oled.show()
print("Should see a checkerboard pattern")
time.sleep(3)

oled.fill(0)
oled.show()

print("\n" + "=" * 40)
print("RESULTS:")
print("Did you see the patterns clearly?")
print("Or was everything just noise?")
print("=" * 40)
