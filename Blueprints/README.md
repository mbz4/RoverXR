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

## BOM

| Count | Type | Length |
|-------|------|--------|
| 6     | M3   | 5mm    |
| 4     | M3   | 12mm   |
| 4     | M3   | 8mm    |

## To-Do:

- add godot setup instructions
- add rover setup instructions
- add Quest2 setup instructions
- add rover mod kit instructions
- add pi zero flashing/config instructions