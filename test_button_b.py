# test_button_b.py
# Test Button B functionality

from machine import Pin
import time

print("=" * 50)
print("Button B Test (GPIO 5)")
print("=" * 50)
print("Press Button B - you should see messages below")
print("Press Ctrl+C to exit")
print("=" * 50)

btnB = Pin(5, Pin.IN, Pin.PULL_UP)
btnB_last = True

try:
    while True:
        btnB_current = btnB.value()

        # Print current state
        print(f"Button B state: {btnB_current} (0=pressed, 1=released)", end='\r')

        # Detect button press
        if btnB_last and not btnB_current:
            print("\n✓ BUTTON B PRESSED!                    ")

        btnB_last = btnB_current
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n" + "=" * 50)
    print("Test stopped")
    print("=" * 50)
