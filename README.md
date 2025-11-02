# Kitsune - a Nine-Tailed Buzzer System

Kitsune is a lockout buzzer system designed by myself (Aisling Skeet). I started this project because lockout buzzer systems are ridiculously expensive for a relatively simple piece of hardware, and college quizbowl teams tend not to be absolutely flush with cash. The most common buzzer set in the UK retails for almost twice the price of a Kitsune set, and doesn't even come in fun colours! This throws a massive barrier in the way of new quiz societies. The other reason for the project is that I'd like to make a bit of extra cash, both for myself and for Durham Uni Quiz Society. Win-win!

If you're interested in buying a Kitsune set, please email me at ash.skeet@pobox.com or message amekyras on Discord. I sell them fully assembled in any filament colour I can get my hands on, with all necessary parts included save a USB-C cable (your phone charger probably works fine). I can add customisations (e.g. your society logo) for a small fee (or free if it's very simple). *I can also make the clear acrylic version pictured at the bottom of the page, but this was originally just a show piece and I don't have regular laser cutter access, so I'll need a longer lead time.*




# END OF 2025 CLEARANCE SALE!!!! WHILE STOCKS LAST!!!!
- Kitsune v0.3 - £120
- Kitsune++ v0.1 - £160
- These do NOT include cables, add £10 for cables (Standard TRS 3.5mm audio cables, 9 for v0.3 and 12 for ++, you can reuse old ones you have lying around)

## Versions

      
- Kitsune v0.3 - **I strongly recommend this version or the Plus Plus, the new jacks are much more resilient to being bashed around**
  - One central box with speaker and USB-C connection, PJ306 metal audio jacks to connect buzzers
  - Nine 'tails' - smaller buzzer boxes connected via 3.5mm audio cables
  - One tail is used as the moderator's control box to initialise and reset the system
  - Complete lockout controlled by Raspberry Pi Pico
  - Indicator lights on buzzer boxes as well as on central box indicate which player has buzzed
  - DIP switch allows control of debug mode, mute, speaker test, and optional autoreset
  
- Kitsune++ v0.1
  - Ten-player version of Kitsune v0.3
 
## Upcoming version

- Kitsune++ v1.0
  - USB-C ports allowing daisychaining of buzzer boxes (under development)
  - Breakouts for all connector jacks and USB ports
  - Increased buzzer voltage 
  - Redesigned tail PCBs and housings for resilience
  - For hackers, breakouts and solder jumpers allow you to design your own buzzer boxes with e.g. different buttons, different LEDs, etc


## Older versions, no longer available:
- Kitsune v0.1 - no longer available
  - One central box with speaker and USB connection
  - Nine 'tails' - smaller buzzer boxes connected via 3.5mm audio cables
  - One tail is used as the moderator's control box to initialise and reset the system
  - Complete lockout controlled by Raspberry Pi Pico
  - Debug jumper to test all ports and boxes
   
- Kitsune v0.2 - no longer available
  - All of the above, plus:
  - Additional onboard LEDS to provide a secondary indication mechanism
  - New JST-XH port to allow external battery usage (tested with 1x9V, should work with multiple AAs in series)
  - New JST-XH port breaking out UART pins
  - Debug jumper replaced with 6-way DIP switch, controlling (left to right)
    - Debug mode
    - Speaker mute
    - Speaker test
    - Automatic reset

## Prices:

Kitsune v0.3 - £150

Kitsune++ v0.1 - £185 (comes with 12 buzzers and 12 cables)

'Grab bag' - Kitsune v0.2 and 9 buzzers, random colours, no cables included - £100

Free collection at certain UK tournaments or domestic shipping £5 (£7.50 for set of two)

USA/other international pricing for a v0.2 set may vary, but is currently whatever the currency conversion amounts to plus however much I need to pay for shipping and packing, not including any import taxes you may need to pay if they apply.

### Discounts

Buying multiple sets - 10% discount for 2 or more sets

No cables needed - minus £10 - Cables used are 3.5mm TRS audio cables, any stereo headphone aux cable should work. This may be particularly useful if located outside the UK, as cables constitute most of the shipping volume and so increase the price.

Compact 'Kit' buzzers using clicky tactile switch rather than red springy switch - minus £10

### Refunds

I can't easily do refunds because I'm one person with not much liquidity. However, if your set isn't working and it's my fault, I'll do everything I can to fix it or replace broken parts, and if I don't, you have my express permission to drag me on social media, accuse me of being a PPG merchant, and claim I'm bad at quiz (true).

### New Societies Scheme

If you've founded a new quizbowl society and don't yet have a buzzer set, and your society is unable to pay full price for a Kitsune set, please let me know and we might be able to work out a discount or a free set. More quizbowl societies = a bigger UK quizbowl scene!

## Maintenance

There shouldn't really be any need to do anything, but if you encounter issues, Kitsune can easily be disassembled. 

The central box is held together with four M3x20 BHCS into M3x4x5 (VORON standard) heat-set inserts, which can be unscrewed with a 2mm hex driver. Take care when separating the top and bottom halves - the buzzer attaches to the mainboard via a JST-XH 2-pin connector, which can be removed to separate all the parts.

Individual buzzer boxes are held together by two M2x10 (M2x8, M2x12 also work) SHCS self-tapping screws. These can be unscrewed with a 1.5mm hex driver, **but this is not recommended unless the buzzer has stopped working.** As these screws are self-tapping, screwing them in several times or too tight can eventually lead to the thread being stripped from the plastic. Only tighten them down as much as necessary to secure the buzzer box.

If the LED on the buzzer box stops working, check that the legs are still soldered to the PJ-320A connector inside the box, and resolder if necessary. The LED is not glued into place so it may shift in its slot in the top of the box, but this is normal and not cause for concern. The PJ-320A connector is also not glued, but is press-fit into the box bottom.

Later buzzer boxes have a custom mini PCB to hold the jack, LED, and button, this eliminates any issues with the LED coming loose.

If the buzzer itself (cylinder on the main box) comes loose in its press-fit slot, it can be secured with a _tiny_ dab of superglue on the side before reinserting it.

### Firmware updates

If, for some reason, you need to reinstall the Kitsune program on the board, this can be done using an IDE such as Thonny or VSCode with the MicroPico extension installed. If you have somehow managed to remove MicroPython from the Pico, it can be reflashed by powering it on or resetting whilst the BOOT button is depressed, and then copying the MicroPython UF2 file to the USB device that will appear on your computer. Of course, if you want to change how Kitsune works, go wild - it's all written in Python, somewhat messy but should be broadly intelligible.

## Credits and disclaimers
I've made this project open-source under a modified Commons Clause. This means that you can make your own Kitsune set, but not sell it. I'm not a lawyer, so in case I've done anything wrong, in plain English - _please don't sell Kitsunes_.

Yes, I know that the code and photography are messy. I'm a psych student, not an engineer.

Many thanks to https://github.com/james1236/buzzer_music for enabling me to include an easter egg or two :)

Absolutely enormous thanks to the Sanjay Mortimer Foundation for supporting me in building these - check them out, they're a fantastic charity! https://www.sanjaymortimerfoundation.org/

TODO: implement USB device identity, to work with buzzin.live etc

## Photos
### Kitsune
![PXL_20241107_222718396](https://github.com/user-attachments/assets/b72bb5ca-9fba-4505-bb74-53a440e6cba6)
![PXL_20241111_130336351 MP](https://github.com/user-attachments/assets/2092b343-8ded-4a94-a322-e174ae3cba6e)
![PXL_20241031_170913548 MP](https://github.com/user-attachments/assets/c04d00e0-4f06-4814-b404-43c0fe9254da)
![PXL_20241231_172731974](https://github.com/user-attachments/assets/e08e6825-bfb9-4bc6-9257-21823b58a606)
![PXL_20250115_020840728 MP](https://github.com/user-attachments/assets/0f0f1921-f110-4ca0-b8ef-4f92146caa6f)

### Kitsune++
![top](https://github.com/user-attachments/assets/4ca15b17-23c5-4ac3-8665-f49d09c70d24)
![bottom](https://github.com/user-attachments/assets/86120f3d-11bd-4be6-ae94-9833517a85d7)
![frontright](https://github.com/user-attachments/assets/0ea4c165-09c4-4595-bd00-d722461d5031)
![rearleft](https://github.com/user-attachments/assets/ee98e576-ab96-45c8-9e36-2d8af2ed5cb1)

![1000017404](https://github.com/user-attachments/assets/bd281261-d5b0-48f5-8d10-aa4a35c9102d)

![1000017403](https://github.com/user-attachments/assets/003a1c4b-e839-482c-b014-1469a85f4737)


