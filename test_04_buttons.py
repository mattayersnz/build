# test_04_buttons.py
# Button Input Test

from machine import Pin
import time

print("=" * 40)
print("Test 04: Button Input Test")
print("=" * 40)

try:
    print("Step 1: Initialize button pins...")
    print("  GPIO 5 = Button A (Start)")
    print("  GPIO 6 = Button B (Stop)")
    print("  GPIO 9 = Button C (Reset)")

    btnA = Pin(5, Pin.IN, Pin.PULL_UP)
    btnB = Pin(6, Pin.IN, Pin.PULL_UP)
    btnC = Pin(9, Pin.IN, Pin.PULL_UP)
    print("  ✓ Buttons initialized with pull-up resistors")

    print("\nStep 2: Reading button states...")
    print("  Active LOW (pressed = 0, released = 1)")
    print("\nInitial states:")
    print(f"  Button A (GPIO 5): {btnA.value()}")
    print(f"  Button B (GPIO 6): {btnB.value()}")
    print(f"  Button C (GPIO 9): {btnC.value()}")

    print("\n" + "=" * 40)
    print("Interactive Button Test")
    print("=" * 40)
    print("Press buttons A, B, or C")
    print("Press all three buttons together to exit")
    print("-" * 40)

    last_states = [1, 1, 1]  # All released initially

    for _ in range(300):  # Run for about 30 seconds
        states = [btnA.value(), btnB.value(), btnC.value()]

        # Check Button A
        if last_states[0] == 1 and states[0] == 0:
            print("✓ Button A PRESSED")
        elif last_states[0] == 0 and states[0] == 1:
            print("  Button A released")

        # Check Button B
        if last_states[1] == 1 and states[1] == 0:
            print("✓ Button B PRESSED")
        elif last_states[1] == 0 and states[1] == 1:
            print("  Button B released")

        # Check Button C
        if last_states[2] == 1 and states[2] == 0:
            print("✓ Button C PRESSED")
        elif last_states[2] == 0 and states[2] == 1:
            print("  Button C released")

        # Exit condition: all three pressed
        if states[0] == 0 and states[1] == 0 and states[2] == 0:
            print("\n" + "=" * 40)
            print("All buttons pressed - exiting test")
            print("=" * 40)
            break

        last_states = states
        time.sleep(0.1)  # 100ms polling

    print("\n" + "=" * 40)
    print("TEST COMPLETED")
    print("=" * 40)
    print("\nIf you saw button press messages, buttons are working!")

except Exception as e:
    print("\n" + "=" * 40)
    print("TEST FAILED")
    print(f"Error: {e}")
    print("=" * 40)
    import sys
    sys.print_exception(e)
