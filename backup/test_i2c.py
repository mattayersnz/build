from machine import Pin, I2C
import time

# Try different I2C configurations for Adafruit RP2040
configs = [
    {"name": "I2C0 (GP0/GP1)", "bus": 0, "scl": 1, "sda": 0},
    {"name": "I2C1 (GP2/GP3)", "bus": 1, "scl": 3, "sda": 2},
    {"name": "I2C1 (GP3/GP2)", "bus": 1, "scl": 2, "sda": 3},
]

for config in configs:
    try:
        print(f"\nTrying {config['name']}...")
        i2c = I2C(config['bus'], scl=Pin(config['scl']), sda=Pin(config['sda']), freq=400000)
        devices = i2c.scan()

        if devices:
            print(f"✓ Found {len(devices)} device(s):")
            for device in devices:
                print(f"  - Address: 0x{device:02x} ({device})")
        else:
            print("  No devices found")
    except Exception as e:
        print(f"  Error: {e}")

print("\nScan complete!")
