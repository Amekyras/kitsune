import machine
import switchboard
import utime
from factory import init_hardware, init_ctrl
from engine import kitsune_engine, player_box
from pinouts import board_pins, firmware_version
import os
from lib.line_clear import clear_line
import micropython
import sys

micropython.alloc_emergency_exception_buf(100)
try:

# 1. Setup

    player_data, switches, mcp = init_hardware() # shim pins, read switches, init mcp

    control_button, control_led = init_ctrl(mcp)


    cfg = switchboard.runtime_config(switches) # setup runtime config with user_cfg data and switch states
    engine = kitsune_engine(cfg, control_led) # init engine with runtime config


    players = [player_box(id=p['id'], button_obj=p['btn'], led_obj=p['led'], engine=engine, irq=True) for p in player_data]


    print(os.uname()) # type: ignore #linter is wrong

    print("Kitsune Version:", firmware_version)

    print ("Pinout:", board_pins["name"])


    
    engine.buzz_startup()


    # do debug
    if cfg.debug:
        print("DEBUG MODE ENABLED")

        

        while True:
            on_list = []
            off_list = []
            for p in players:
                if p.button.value() == 1:
                    on_list.append(p.id)
                    p.update_led(1)
                else:
                    off_list.append(p.id)
                    p.update_led(0)
            if control_button.value() == 1:
                on_list.append("CTRL")
                control_led.on()
            else:
                off_list.append("CTRL")
                control_led.off()

            for s in switches:
                if s.value() == 1:
                    on_list.append(f"Switch {switches.index(s)+1}")
                else:
                    off_list.append(f"Switch {switches.index(s)+1}")
            print(f"ON: {on_list}")
            print(f"OFF: {off_list}")
            utime.sleep(0.1)
            clear_line(2)




    print("Unlock to start")

    #while True:
    #    try:
    #        engine.buzz()
    #    except Exception as e:
    #        cfg.buzzer.duty_u16(0)
    #        sys.print_exception(e)
    #        break

    #cfg.buzzer.deinit()
    #cfg.buzzer_pin.high()
    # 2. Main Loop
    while True:
        # If the MCP is used for buttons, we poll them here
        # If using IRQs on native pins, this loop stays nearly empty!
        if engine.locked:
            # Check for Reset button press
            if control_button.value() == 1:
                engine.reset()
            pass                                 

except Exception as e:
    #cfg.buzzer.duty_u16(0)
    sys.print_exception(e)
    #machine.reset()