from machine import Pin, I2C, Timer
import time
from ssd1306 import SSD1306_I2C

# ----------------------------
# I2C + OLED Setup
# ----------------------------
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)  # Feather RP2040 SCL=GPIO3, SDA=GPIO2

# Initialize display with proper reset
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

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
btnA = Pin(5, Pin.IN, Pin.PULL_UP)  # Button A – Start
btnB = Pin(6, Pin.IN, Pin.PULL_UP)  # Button B – Stop
btnC = Pin(9, Pin.IN, Pin.PULL_UP)  # Button C – Reset

# Button state tracking for debouncing
btnA_last = True
btnB_last = True
btnC_last = True

# ----------------------------
# Timer State
# ----------------------------
running = False
start_time = 0
elapsed = 0

# ----------------------------
# Helper: Format time as MM:SS.hh
# ----------------------------
def format_time(ms):
    total_seconds = ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    hundredths = (ms % 1000) // 10
    return "{:02d}:{:02d}.{:02d}".format(minutes, seconds, hundredths)

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
        oled.text("RUNNING", 40, 50)
    else:
        oled.text("STOPPED", 40, 50)

    oled.show()

# ----------------------------
# Main Loop
# ----------------------------
update_display()

while True:
    # --- Button A: Start (detect button press on falling edge) ---
    btnA_current = btnA.value()
    if btnA_last and not btnA_current:   # button just pressed
        if not running:
            running = True
            start_time = time.ticks_ms() - elapsed
            update_display()
    btnA_last = btnA_current

    # --- Button B: Stop ---
    btnB_current = btnB.value()
    if btnB_last and not btnB_current:   # button just pressed
        if running:
            running = False
            elapsed = time.ticks_ms() - start_time
            update_display()
    btnB_last = btnB_current

    # --- Button C: Reset ---
    btnC_current = btnC.value()
    if btnC_last and not btnC_current:   # button just pressed
        running = False
        elapsed = 0
        update_display()
    btnC_last = btnC_current

    # --- If running, update elapsed ---
    if running:
        elapsed = time.ticks_ms() - start_time
        update_display()

    time.sleep_ms(50)
