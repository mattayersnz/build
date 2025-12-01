# test_03_pixel.py
# Single Pixel Test - Visual Confirmation

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

print("=" * 40)
print("Test 03: Single Pixel Test")
print("=" * 40)

try:
    print("Step 1: Initialize display...")
    i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
    oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)
    print("  ✓ Display initialized")

    print("\nStep 2: Clear display...")
    oled.fill(0)
    oled.show()
    print("  ✓ Display cleared")
    print("  >> Look at display - should be completely blank")
    time.sleep(2)

    print("\nStep 3: Draw center pixel...")
    oled.pixel(64, 32, 1)  # Center of 128x64 display
    oled.show()
    print("  ✓ Center pixel set at (64, 32)")
    print("  >> Look for a single pixel in the center")
    time.sleep(2)

    print("\nStep 4: Draw 4 corner pixels...")
    oled.pixel(0, 0, 1)      # Top-left
    oled.pixel(127, 0, 1)    # Top-right
    oled.pixel(0, 63, 1)     # Bottom-left
    oled.pixel(127, 63, 1)   # Bottom-right
    oled.show()
    print("  ✓ Corner pixels set")
    print("  >> Look for 5 pixels total (center + 4 corners)")
    time.sleep(2)

    print("\nStep 5: Fill entire display...")
    oled.fill(1)
    oled.show()
    print("  ✓ Display filled with white")
    print("  >> Display should be completely white")
    time.sleep(2)

    print("\nStep 6: Clear display again...")
    oled.fill(0)
    oled.show()
    print("  ✓ Display cleared")

    print("\n" + "=" * 40)
    print("TEST PASSED")
    print("=" * 40)
    print("\n**IMPORTANT**: Did you see pixels on the display?")
    print("If yes - display is working!")
    print("If no - check connections and try adjusting contrast")

except Exception as e:
    print("\n" + "=" * 40)
    print("TEST FAILED")
    print(f"Error: {e}")
    print("=" * 40)
    import sys
    sys.print_exception(e)
