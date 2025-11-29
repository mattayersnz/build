from machine import Pin, I2C
import time
from ssd1306 import SSD1306_I2C

# Initialize I2C
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)

# Initialize display with explicit address
try:
    oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

    # Clear the display first
    oled.fill(0)
    oled.show()
    time.sleep(0.5)

    # Test with simple text
    oled.text("Hello!", 0, 0)
    oled.text("RP2040", 0, 20)
    oled.text("Works!", 0, 40)
    oled.show()

    print("Display initialized successfully!")

except Exception as e:
    print(f"Error: {e}")
