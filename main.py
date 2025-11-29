from machine import Pin, I2C, Timer
import time
from ssd1306 import SSD1306_I2C

# ----------------------------
# I2C + OLED Setup
# ----------------------------
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)  # Feather RP2040 SCL=GPIO3, SDA=GPIO2
oled = SSD1306_I2C(128, 64, i2c)

# ----------------------------
# Button Setup (active LOW)
# ----------------------------
btnA = Pin(5, Pin.IN, Pin.PULL_UP)  # Button A – Start
btnB = Pin(6, Pin.IN, Pin.PULL_UP)  # Button B – Stop
btnC = Pin(9, Pin.IN, Pin.PULL_UP)  # Button C – Reset

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
    # --- Button A: Start ---
    if not btnA.value():   # active LOW
        if not running:
            running = True
            start_time = time.ticks_ms() - elapsed
            update_display()
        time.sleep_ms(200)  # debounce

    # --- Button B: Stop ---
    if not btnB.value():
        if running:
            running = False
            elapsed = time.ticks_ms() - start_time
            update_display()
        time.sleep_ms(200)

    # --- Button C: Reset ---
    if not btnC.value():
        running = False
        elapsed = 0
        update_display()
        time.sleep_ms(200)

    # --- If running, update elapsed ---
    if running:
        elapsed = time.ticks_ms() - start_time
        update_display()
        time.sleep_ms(50)
