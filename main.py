from machine import Pin, I2C, Timer
import time
from sh1107 import SH1107_I2C

# ----------------------------
# I2C + OLED Setup
# ----------------------------
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)  # Feather RP2040 SCL=GPIO3, SDA=GPIO2

# Initialize display with SH1107 driver (address 0x3c, rotated 180°)
oled = SH1107_I2C(128, 64, i2c, address=0x3c, rotate=180)
oled.sleep(False)  # Wake display

# Force display off, clear buffer, then turn back on
oled.poweroff()
time.sleep(0.1)
oled.fill(0)
oled.poweron()
oled.show()
time.sleep(0.2)

# ----------------------------
# Button Setup (active LOW)
# ----------------------------
btnA = Pin(9, Pin.IN, Pin.PULL_UP)  # Button A – Start/Stop/Reset (GPIO 9)

# Button state tracking for long-press detection
btnA_last = True
btnA_press_start = 0
btnA_was_long_press = False

# ----------------------------
# Timer State
# ----------------------------
running = False
start_time = 0
elapsed = 0

# ----------------------------
# Helper: Format time as SS.thm (seconds.tenths-hundredths-milliseconds)
# ----------------------------
def format_time(ms):
    total_seconds = ms // 1000
    tenths = (ms % 1000) // 100
    hundredths = (ms % 100) // 10
    thousandths = ms % 10
    return "{:02d}.{:01d}{:01d}{:01d}".format(total_seconds, tenths, hundredths, thousandths)

# ----------------------------
# OLED Update Function
# ----------------------------
def update_display():
    oled.fill(0)
    oled.text("LAP TIMER", 20, 0)

    # Timer display
    oled.text(format_time(elapsed), 20, 25)

    # Status text
    if running:
        oled.text("RUNNING", 20, 50)
    else:
        oled.text("STOPPED", 20, 50)

    oled.show()

# ----------------------------
# Main Loop
# ----------------------------
update_display()

while True:
    # --- Button A: Single button with long-press detection ---
    btnA_current = btnA.value()

    # Detect button press (falling edge)
    if btnA_last and not btnA_current:
        # Button just pressed - record time
        btnA_press_start = time.ticks_ms()
        btnA_was_long_press = False

    # Check if button is being held down
    if not btnA_current:  # Button is currently pressed
        press_duration = time.ticks_diff(time.ticks_ms(), btnA_press_start)
        if press_duration >= 1000 and not btnA_was_long_press:
            # Long press detected (1 second) - RESET
            btnA_was_long_press = True
            running = False
            elapsed = 0
            update_display()

    # Detect button release (rising edge)
    if not btnA_last and btnA_current:
        if not btnA_was_long_press:
            # Short press - START/STOP TOGGLE
            if running:
                # Stop/Pause timer (preserve elapsed time)
                running = False
                elapsed = time.ticks_ms() - start_time
            else:
                # Start/Resume timer
                running = True
                start_time = time.ticks_ms() - elapsed
            update_display()

    btnA_last = btnA_current

    # --- If running, update elapsed ---
    if running:
        elapsed = time.ticks_ms() - start_time
        update_display()

    time.sleep_ms(50)
