# test_02_init.py
# Display Initialization Test

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

print("=" * 40)
print("Test 02: Display Initialization")
print("=" * 40)

try:
    print("Step 1: Initialize I2C bus...")
    i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
    print("  ✓ I2C initialized")

    print("\nStep 2: Create display object...")
    print("  Size: 128x64 pixels")
    print("  Address: 0x3c")
    oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)
    print("  ✓ Display object created")

    print("\nStep 3: Test basic display commands...")
    oled.fill(0)
    print("  ✓ fill(0) - clear framebuffer")

    oled.show()
    print("  ✓ show() - update display")

    print("\n" + "=" * 40)
    print("TEST PASSED")
    print("=" * 40)
    print("\nDisplay initialized successfully!")
    print("The display should now be blank/clear.")

except Exception as e:
    print("\n" + "=" * 40)
    print("TEST FAILED")
    print(f"Error: {e}")
    print("=" * 40)
    import sys
    sys.print_exception(e)
