# Copilot instructions for Kitsune

## Big-picture architecture
- Firmware is MicroPython for Raspberry Pi Pico. Entry point is [Firmware/main.py](Firmware/main.py) which initializes hardware, builds runtime config, and starts the lockout loop.
- Hardware init lives in [Firmware/factory.py](Firmware/factory.py): it selects pinout from [Firmware/pinouts.py](Firmware/pinouts.py), optionally sets up MCP23017 over I2C, and wraps GPIO/MCP pins with `UnifiedPin` from [Firmware/lib/shims.py](Firmware/lib/shims.py).
- Game logic is in [Firmware/engine.py](Firmware/engine.py): `player_box` debounces button IRQs and calls `kitsune_engine.handle_buzz()` via `micropython.schedule`; engine controls lockout, LEDs, and buzzer timing.
- Runtime settings come from [Firmware/switchboard.py](Firmware/switchboard.py) and [Firmware/user_cfg.py](Firmware/user_cfg.py): DIP switches set debug/mute/test/autoreset; `user_cfg.py` defines volume/frequency/LED colors.
- LEDs use NeoPixel in `runtime_config` and per-player LEDs via `UnifiedPin`. Buzzer startup jingle uses `lib/buzzer_music.py`.

## Firmware workflow & environment
- MicroPython-only: keep APIs compatible with `machine`, `micropython`, `utime`, and `neopixel` (see [typings/](typings/) for stubs).
- The README notes firmware updates are done by copying files to the Pico (e.g., via Thonny or VS Code MicroPico). Avoid CPython-only dependencies.

## Project-specific conventions & patterns
- IRQ handlers must be tiny; use `micropython.schedule()` to defer work (see `player_box._handle_press()` in [Firmware/engine.py](Firmware/engine.py)).
- Use `UnifiedPin` for any pin that may come from MCP23017 so code works for both native GPIO and expander pins (see [Firmware/factory.py](Firmware/factory.py)).
- Board selection is centralized: update `board_pins` in [Firmware/pinouts.py](Firmware/pinouts.py) instead of scattering pin changes.
- Volume is a percentage in `user_cfg.py` and converted to duty cycle in `runtime_config` (see [Firmware/switchboard.py](Firmware/switchboard.py)).

## Integration points
- MCP23017 I2C expander: initialized in `init_mcp()` with SDA=20/SCL=21; used when `board_pins["mcp"]` is true (see [Firmware/factory.py](Firmware/factory.py)).
- NeoPixel is a single LED at `pixel_pin` defined in [Firmware/pinouts.py](Firmware/pinouts.py).

## Tests & utilities
- Hardware smoke tests live under [Tests/](Tests/) (e.g., PWM buzzer, MCP I2C, timers). These are direct-on-device scripts, not automated unit tests.

## Specific instructions
 - When answering chat questions, utilise the full context of the project - either locally or on GitHub, whichever is faster. Consider all files, and check that a certain functionality exists before making any recommendations. If you are unsure about something, ask for clarification instead of making assumptions.