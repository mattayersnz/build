# test_all_configs.py
# Try all COM pin configurations systematically

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

configs = [
    (0x02, "Sequential, no remap"),
    (0x12, "Alternative, no remap"),
    (0x22, "Sequential, with remap"),
    (0x32, "Alternative, with remap"),
]

print("=" * 40)
print("Testing All COM Pin Configurations")
print("=" * 40)

i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)

for value, desc in configs:
    print(f"\nTrying 0x{value:02X}: {desc}")
    print("-" * 40)

    # Manually set COM pin config
    i2c.writeto(0x3c, bytes([0x00, 0xDA]))  # SET_COM_PIN_CFG
    i2c.writeto(0x3c, bytes([0x00, value]))

    # Initialize display
    oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

    # Fill with white
    oled.fill(1)
    oled.show()

    print(f"Display filled with config 0x{value:02X}")
    print("Check display - is it clean?")
    time.sleep(3)

    # Clear
    oled.fill(0)
    oled.show()
    time.sleep(1)

print("\n" + "=" * 40)
print("Which configuration (if any) looked best?")
print("=" * 40)
