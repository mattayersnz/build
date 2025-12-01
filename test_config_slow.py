# test_config_slow.py
# Test COM pin configurations one at a time with clear visual feedback

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

configs = [
    (0x02, "Config 1: Sequential, no remap (0x02)"),
    (0x12, "Config 2: Alternative, no remap (0x12) [DEFAULT]"),
    (0x22, "Config 3: Sequential, with remap (0x22)"),
    (0x32, "Config 4: Alternative, with remap (0x32)"),
]

print("=" * 50)
print("OLED Display Configuration Test")
print("=" * 50)
print("\nWatch your display for each configuration:")
print("- First: blank screen")
print("- Then: 'HELLO' text in top-left")
print("- Then: full white screen")
print("- Finally: blank again")
print("\nNote which config shows clean, readable text!")
print("=" * 50)

i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)

for value, desc in configs:
    print(f"\n{'='*50}")
    print(desc)
    print('='*50)

    # Set COM pin configuration manually
    i2c.writeto(0x3c, bytes([0x00, 0xDA]))  # SET_COM_PIN_CFG command
    i2c.writeto(0x3c, bytes([0x00, value]))  # Set value

    # Initialize display
    oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

    # Proper power cycle sequence
    oled.poweroff()
    time.sleep(0.1)
    oled.fill(0)
    oled.poweron()
    oled.show()

    print("Step 1: Blank screen...")
    time.sleep(2)

    # Draw text
    oled.fill(0)
    oled.text('HELLO', 0, 0)
    oled.text('Testing', 0, 10)
    oled.text(f'Config: 0x{value:02X}', 0, 20)
    oled.show()
    print("Step 2: Showing 'HELLO' text...")
    print(">>> LOOK AT DISPLAY NOW <<<")
    time.sleep(5)

    # Fill white
    oled.fill(1)
    oled.show()
    print("Step 3: Full white screen...")
    time.sleep(3)

    # Clear
    oled.fill(0)
    oled.show()
    print("Step 4: Cleared")
    time.sleep(1)

print("\n" + "=" * 50)
print("TEST COMPLETE")
print("=" * 50)
print("\nWhich configuration showed clean, readable text?")
print("1 = 0x02")
print("2 = 0x12 (default)")
print("3 = 0x22")
print("4 = 0x32")
