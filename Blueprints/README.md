# CAD, ELE, FW, HOW-TO

# Pi-Side Setup

0. flash Raspbian Lite (32-bit) onto SD Card (class 10 recommended), then run

`sudo apt-get update`

`sudo apt-get upgrade`

`sudo raspi-config`

1. get the repo to the pi

`git clone https://github.com/mbz4/edu_teleop_demo.git`

2. python ./Blueprints/stream_mjpeg_ws.py

# VR setup

1. get scene apk to your Meta Quest 2

2. run apk

# M5 Rover C setup

1. print mod kit file 

- gcode (sliced for Prusa MK3S)

`Blueprints/CAD/32g_rover_mod_kit_0.3mm_PLA_MK3S_2h12m.gcode` 

- 3mf model file

`Blueprints/CAD/rover_mod_kit.3mf`

2. assemble mod kit

 - [Bill of materials](/CAD/README.md)
 - ![Artefact, v2, with screws](/CAD/v2_w_screws.png)

3. flash firmware, can use Arduino IDE (M5 Stick C library)

- connect rover M5 Stick C to PC
- open & flash:

`Blueprints/rover_FW/Master/Master.ino`

- disconnect from PC and install Master Stick to Rover
- connect remote M5 Stick C to PC
- open & flash:

`Blueprints/rover_FW/Remote/Remote.ino`

- disconnect from PC and install Remote Stick to Remote Controller
- use power switches on remote & rover
- press and hold for 4 seconds the lower left side button on both M5 Stick C's to turn them on
- press and hold for 4 seconds the 'M5' button on Remote controller, once the Master MAC address is shown
- rover can now be remotely operated using remote

## To-Do:

- add godot setup instructions
- add rover setup instructions
- add Quest2 setup instructions
- add rover mod kit instructions
- add pi zero flashing/config instructions