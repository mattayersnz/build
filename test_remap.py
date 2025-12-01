# test_remap.py
# Test different segment remap and COM scan direction combinations

from machine import Pin, I2C
import time

print("=" * 50)
print("Segment Remap and COM Scan Direction Test")
print("=" * 50)
print("\nTesting 4 combinations to fix half-screen noise:")
print("Watch for clean, readable text!")
print("=" * 50)

i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)

# Different combinations of segment remap and COM scan
configs = [
    (0xA0, 0xC0, "Config 1: SEG normal (0xA0), COM normal (0xC0)"),
    (0xA1, 0xC0, "Config 2: SEG remap (0xA1), COM normal (0xC0) [DEFAULT]"),
    (0xA0, 0xC8, "Config 3: SEG normal (0xA0), COM reverse (0xC8)"),
    (0xA1, 0xC8, "Config 4: SEG remap (0xA1), COM reverse (0xC8)"),
]

def init_display_with_config(seg_remap, com_dir):
    """Initialize display with specific remap settings"""
    cmds = [
        0xAE,        # Display OFF
        0x20, 0x00,  # Memory addressing mode: horizontal
        0x40,        # Start line 0
        seg_remap,   # Segment remap (0xA0 or 0xA1)
        0xA8, 0x3F,  # Multiplex ratio (64)
        com_dir,     # COM scan direction (0xC0 or 0xC8)
        0xD3, 0x00,  # Display offset: 0
        0xDA, 0x12,  # COM pins config: 0x12
        0xD5, 0x80,  # Clock divide
        0xD9, 0xF1,  # Pre-charge
        0xDB, 0x30,  # VCOM deselect
        0x81, 0xFF,  # Contrast: maximum
        0xA4,        # Output follows RAM
        0xA6,        # Normal display (not inverted)
        0x8D, 0x14,  # Charge pump ON
        0xAF,        # Display ON
    ]

    for cmd in cmds:
        i2c.writeto(0x3c, bytes([0x00, cmd]))

def clear_display():
    """Clear display memory"""
    # Set addressing window to full display
    i2c.writeto(0x3c, bytes([0x00, 0x21, 0, 127]))  # Column addr
    i2c.writeto(0x3c, bytes([0x00, 0x22, 0, 7]))    # Page addr
    # Write zeros to all memory
    for _ in range(8):  # 8 pages
        data = bytes([0x40] + [0x00] * 128)  # 0x40 = data mode
        i2c.writeto(0x3c, data)

def draw_test_pattern():
    """Draw simple test pattern"""
    # Set addressing window
    i2c.writeto(0x3c, bytes([0x00, 0x21, 0, 127]))  # Column addr
    i2c.writeto(0x3c, bytes([0x00, 0x22, 0, 7]))    # Page addr

    # Draw pattern: first 2 pages white, rest black
    for page in range(8):
        if page < 2:
            # White rows (top of screen)
            data = bytes([0x40] + [0xFF] * 128)
        else:
            # Black rows
            data = bytes([0x40] + [0x00] * 128)
        i2c.writeto(0x3c, data)

for seg_remap, com_dir, desc in configs:
    print(f"\n{'='*50}")
    print(desc)
    print('='*50)

    # Initialize with this config
    init_display_with_config(seg_remap, com_dir)
    time.sleep(0.5)

    # Clear
    print("Step 1: Clearing display...")
    clear_display()
    time.sleep(2)

    # Draw test pattern
    print("Step 2: Drawing test pattern...")
    print(">>> LOOK: Should show WHITE bar at TOP <<<")
    draw_test_pattern()
    time.sleep(5)

    # Clear again
    clear_display()
    time.sleep(1)

print("\n" + "=" * 50)
print("TEST COMPLETE")
print("=" * 50)
print("\nWhich config showed a clean WHITE bar at the TOP?")
print("1 = SEG normal, COM normal")
print("2 = SEG remap, COM normal [DEFAULT]")
print("3 = SEG normal, COM reverse")
print("4 = SEG remap, COM reverse")
