# test_sh1107_display.py
# Test SH1107 display driver

from machine import Pin, I2C
from sh1107 import SH1107_I2C
import time

print("=" * 50)
print("SH1107 Display Test")
print("=" * 50)

try:
    print("Step 1: Initialize I2C and SH1107 display...")
    i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
    oled = SH1107_I2C(128, 64, i2c, address=0x3c)
    oled.sleep(False)  # Wake display
    print("  ✓ Display initialized at address 0x3c")

    print("\nStep 2: Clear display...")
    oled.fill(0)
    oled.show()
    print("  ✓ Display cleared")
    time.sleep(2)

    print("\nStep 3: Display 'HELLO' text...")
    oled.fill(0)
    oled.text('HELLO', 0, 0)
    oled.text('SH1107', 0, 10)
    oled.text('Driver', 0, 20)
    oled.text('Works!', 0, 30)
    oled.show()
    print("  ✓ Text displayed")
    print("  >>> CHECK DISPLAY - Should show clean text! <<<")
    time.sleep(5)

    print("\nStep 4: Fill display white...")
    oled.fill(1)
    oled.show()
    print("  ✓ Display filled white")
    print("  >>> CHECK DISPLAY - Should be completely white <<<")
    time.sleep(3)

    print("\nStep 5: Draw test pattern...")
    oled.fill(0)
    # Draw a border
    for x in range(128):
        oled.pixel(x, 0, 1)
        oled.pixel(x, 63, 1)
    for y in range(64):
        oled.pixel(0, y, 1)
        oled.pixel(127, y, 1)
    oled.text('BORDER', 40, 28)
    oled.show()
    print("  ✓ Border and text drawn")
    print("  >>> CHECK DISPLAY - Should show border with text <<<")
    time.sleep(5)

    print("\nStep 6: Clear display...")
    oled.fill(0)
    oled.show()
    print("  ✓ Display cleared")

    print("\n" + "=" * 50)
    print("TEST PASSED!")
    print("=" * 50)
    print("\nIf you saw clean text and graphics without noise,")
    print("the SH1107 driver is working correctly!")

except Exception as e:
    print("\n" + "=" * 50)
    print("TEST FAILED")
    print(f"Error: {e}")
    print("=" * 50)
    import sys
    sys.print_exception(e)
