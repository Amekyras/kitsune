# Kitsune - a Nine-Tailed Buzzer System

Kitsune is a lockout buzzer system designed by myself (Aisling Skeet). I started this project because lockout buzzer systems are ridiculously expensive for a relatively simple piece of hardware, and college quizbowl teams tend not to be absolutely flush with cash. The most common buzzer set in the UK retails for almost twice the price of a Kitsune set, and doesn't even come in fun colours! This throws a massive barrier in the way of new quiz societies. The other reason for the project is that I'd like to make a bit of extra cash, both for myself and for Durham Uni Quiz Society. Win-win!

If you're interested in buying a Kitsune set, please email me at ash.skeet@pobox.com or message amekyras on Discord. I sell them fully assembled in any filament colour I can get my hands on, with all necessary parts included save a USB-C cable (your phone charger probably works fine). I can add customisations (e.g. your society logo) for a small fee.

## Versions
- Kitsune v0.1
  - One central box with speaker and USB connection
  - Nine 'tails' - smaller buzzer boxes connected via 3.5mm audio cables
  - One tail is used as the moderator's control box to initialise and reset the system
  - Complete lockout controlled by Raspberry Pi Pico
  - Debug jumper to test all ports and boxes
   
- Kitsune v0.2
  - All of the above, plus:
  - Additional onboard LEDS to provide a secondary indication mechanism
  - New JST-XH port to allow external battery usage (tested with 1x9V, should work with multiple AAs in series)
  - New JST-XH port breaking out UART pins, will be used for connecting two boards together for 16-player mode at a later date
  - Debug jumper replaced with 6-way DIP switch, controlling (left to right)
    - Debug mode
    - Speaker mute
    - Speaker test
    - Automatic reset
    - Multibuzzer branch mode (currently inactive)
    - Multibuzzer main mode (currently inactive)


## Prices:

Kitsune v0.1 - £125 (while stocks last)

Kitsune v0.2 - £150, set of two £275

Free collection at certain UK tournaments or domestic shipping £5

### New Societies Scheme

If you've founded a new  quizbowl society and don't yet have a buzzer set, and your society is unable to pay full price for a Kitsune set, please let me know and we might be able to work out a discount or a free set. More quizbowl societies = a bigger UK quizbowl scene!


## Credits and disclaimers
I've made this project open-source under a modified Commons Clause. This means that you can make your own Kitsune set, but not sell it. I'm not a lawyer, so in case I've done anything wrong, in plain English - _please don't sell Kitsunes_.

Yes, I know that the code and photography are messy. I'm a psych student, not an engineer.

Many thanks to https://github.com/james1236/buzzer_music for enabling me to include an easter egg or two :)

## Photos
![PXL_20241107_222718396](https://github.com/user-attachments/assets/b72bb5ca-9fba-4505-bb74-53a440e6cba6)
![PXL_20241111_130336351 MP](https://github.com/user-attachments/assets/2092b343-8ded-4a94-a322-e174ae3cba6e)
![PXL_20241031_170913548 MP](https://github.com/user-attachments/assets/c04d00e0-4f06-4814-b404-43c0fe9254da)
![PXL_20241231_172731974](https://github.com/user-attachments/assets/e08e6825-bfb9-4bc6-9257-21823b58a606)

