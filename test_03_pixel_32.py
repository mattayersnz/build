# test_03_pixel_32.py
# Test with 128x32 size instead of 128x64

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

print("=" * 40)
print("Test: 128x32 Display Size")
print("=" * 40)

try:
    print("Initializing as 128x32...")
    i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
    oled = SSD1306_I2C(128, 32, i2c, addr=0x3c)  # 32 height instead of 64
    print("  ✓ Display initialized as 128x32")

    print("\nClearing display...")
    oled.fill(0)
    oled.show()
    time.sleep(1)

    print("Filling display with white...")
    oled.fill(1)
    oled.show()
    time.sleep(2)

    print("Drawing test pattern...")
    oled.fill(0)
    oled.rect(0, 0, 128, 32, 1)
    oled.text("128x32", 40, 12, 1)
    oled.show()

    print("\n" + "=" * 40)
    print("Does the display look clean now?")
    print("If yes - you have a 128x32 display")
    print("If no - you have a 128x64 display")
    print("=" * 40)

except Exception as e:
    print(f"Error: {e}")
    import sys
    sys.print_exception(e)
