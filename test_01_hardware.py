# test_01_hardware.py
# Hardware Detection Test - I2C Bus Scan

from machine import Pin, I2C
import time

print("=" * 40)
print("Test 01: Hardware Detection")
print("=" * 40)

try:
    print("Step 1: Initialize I2C bus...")
    print("  GPIO 2 = SDA")
    print("  GPIO 3 = SCL")
    print("  Frequency = 400kHz")

    i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
    print("  ✓ I2C initialized")

    print("\nStep 2: Scan for I2C devices...")
    devices = i2c.scan()

    if len(devices) == 0:
        print("  ✗ No I2C devices found!")
        print("\nTroubleshooting:")
        print("  - Check 3V power connection")
        print("  - Check GND connection")
        print("  - Check SDA (GPIO 2) connection")
        print("  - Check SCL (GPIO 3) connection")
    else:
        print(f"  ✓ Found {len(devices)} device(s):")
        for addr in devices:
            print(f"    - 0x{addr:02x} (decimal: {addr})")

        # Check specifically for OLED at 0x3c
        if 0x3c in devices:
            print("\n  ✓✓ SSD1306 OLED detected at 0x3c!")
        else:
            print(f"\n  ⚠ Expected OLED at 0x3c not found")
            print(f"    Found device(s) at: {[hex(d) for d in devices]}")

    print("\n" + "=" * 40)
    print("TEST PASSED" if 0x3c in devices else "TEST INCOMPLETE")
    print("=" * 40)

except Exception as e:
    print("\n" + "=" * 40)
    print("TEST FAILED")
    print(f"Error: {e}")
    print("=" * 40)
    import sys
    sys.print_exception(e)
