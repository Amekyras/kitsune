#buzzer_pin = 13
status_pin = 25
#control_led = 15
#control_pin = 14
pixel_pin = 23
#tx_pin = 0
#rx_pin = 1






p8_pins = {
    "switch_pins": [28, 23, 22, 12, 11, 10], #v0.2 pins
    "button_pins": [2, 4, 6, 8, 16, 18, 20, 26], #v0.2 pins
    "led_pins": [3, 5, 7, 9, 17, 19, 21, 27], #v0.2 pins
    "ids": ["A1", "A2", "A3", "A4", "B4", "B3", "B2", "B1"],
    "switch_ids": ["switch1", "switch2", "switch3", "switch4", "switch5", "switch6"],
    "buzzer_pin": 13,
    "control_led": 15,
    "control_pin": 14,
    "name": "v0.2/v0.3",
    "daisychain": False,
    "mcp": False
}

p10_pins = {
    "switch_pins": [28, 23, 22, 12], 
    "button_pins": [2, 4, 6, 8, 0, 10, 16, 18, 20, 26], 
    "led_pins": [3, 5, 7, 9, 1, 11, 17, 19, 21, 27], 
    "ids": ["A1", "A2", "A3", "A4", "A5", "B5", "B4", "B3", "B2", "B1"],
    "switch_ids": ["switch1", "switch2", "switch3", "switch4"],
    "buzzer_pin": 13,
    "control_led": 15,
    "control_pin": 14,
    "name": "++ v0.1",
    "daisychain": False,
    "mcp": False
}

p10v1_pins = { #pins for kitsune++ v1.0 board - assign switches (read-once) and LEDs (write-only) to MCP23017
    "switch_pins": [11, 12, 13, 14], # MCP pins 
    "button_pins": [6, 7, 8, 9, 10, 12, 14, 15, 16, 17], 
    "led_pins": [0, 1, 2, 3, 4, 6, 7, 8, 9, 10], # MCP pins
    "ids": ["A1", "A2", "A3", "A4", "A5", "B5", "B4", "B3", "B2", "B1"],
    "switch_ids": ["switch1", "switch2", "switch3", "switch4"],
    "buzzer_pin": 13,
    "control_led": 5, #mcp
    "control_pin": 11,
    "name": "v1.0++",
    "daisychain": True,
    "mcp": True
}


firmware_version = "3.1.0-alpha"

board_pins = p10v1_pins #switch pinouts for ++ board are p10_pins