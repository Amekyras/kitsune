# end user configuration - buzzer volume, buzzer frequency, LED colours

override_vol_default = False  # Set to True to override the default volume for the board (as defined in pinouts.py) with the value below.
volume = 10  # Default volume percentage - interpreted as a percentage of max_volume_duty
# 30 is sweet spot for 5v?
# 7 is sweet spot for 27v at normal volume


freqmod = 100  # Default frequency modulation factor

team_a_colour = (0, 0, 255)  # Blue
team_a_freq_offset = 1.02
team_b_colour = (0, 255, 0)  # Green
team_b_freq_offset = 0.98
def_colour = (255, 0, 0)  # Red
armed_colour = (128, 128, 128)  # Dim white

reset_duration = 10000  # Time (ms) after buzz to reset, only if enabled




### BOARD SPECIFIC CONFIGURATION BELOW - DO NOT EDIT UNLESS YOU KNOW WHAT YOU ARE DOING ###

max_volume_duty = 32768  # Max duty cycle for volume (out of 65535). Increase this if you really want it to be louder.

