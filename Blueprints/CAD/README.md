# CAD Tree

```
📦CAD
 ┣ 📂v1
 ┃ ┣ 📜32g_rover_mod_kit_0.3mm_PLA_MK3S_2h12m.gcode
 ┃ ┣ 📜rover_mod_kit.3mf
 ┃ ┗ 📜v1.png
 ┣ 📂v2
 ┃ ┣ 📂3mf
 ┃ ┃ ┣ 📂deprecated
 ┃ ┃ ┃ ┣ 📜assorted_camera_mounts.3mf
 ┃ ┃ ┃ ┣ 📜camera_mounting_shroud v15.3mf
 ┃ ┃ ┃ ┣ 📜camera_mounting_shroud v16.3mf
 ┃ ┃ ┃ ┣ 📜camera_mounting_shroud_3,04mm_focal_adjust v10.3mf
 ┃ ┃ ┃ ┣ 📜camera_mounting_shroud_3,04mm_focal_adjust v11.3mf
 ┃ ┃ ┃ ┗ 📜rear_port_bumber v32.3mf
 ┃ ┃ ┣ 📜adjustable_camera_shroud_mount_w_lens.3mf
 ┃ ┃ ┣ 📜bumper_maglock_adapter v23.3mf
 ┃ ┃ ┣ 📜bumper_maglock_adapter_cap v23.3mf
 ┃ ┃ ┣ 📜camera_mounting_shroud v21.3mf
 ┃ ┃ ┣ 📜joy_c_remote_adapter v22.3mf
 ┃ ┃ ┣ 📜joy_c_remote_adapter_cap v22.3mf
 ┃ ┃ ┣ 📜maglock_adapter_kit.3mf
 ┃ ┃ ┣ 📜mounting_adapter_v2 v66.3mf
 ┃ ┃ ┗ 📜rear_port_bumber v34.3mf
 ┃ ┣ 📂f3z
 ┃ ┃ ┗ 📜assembly v68.f3z
 ┃ ┣ 📂step
 ┃ ┃ ┣ 📜adjustable_camera_shroud_mount_w_lens.step
 ┃ ┃ ┣ 📜assembly v68.step
 ┃ ┃ ┣ 📜camera_mounting_shroud.step
 ┃ ┃ ┣ 📜mounting_adapter_v2 v66.step
 ┃ ┃ ┗ 📜rear_port_bumber v32.step
 ┃ ┣ 📜38g_full_mod_kit_v2_0.2mm_PLA_MK3S_4h47m.gcode
 ┃ ┣ 📜3g_maglock_adapter_kit_0.2mm_PLA_MK3S_29m.gcode
 ┃ ┣ 📜mod_kit_v2.3mf
 ┃ ┣ 📜v2.png
 ┃ ┗ 📜v2_w_screws.png
 ┣ 📜assembly v77.avi
 ┣ 📜README.md
 ┣ 📜v0_concept_phase.png
 ┣ 📜v1.png
 ┗ 📜v2_w_screws.png
```

# Bill of materials

|Component                       |Description                                                                                                                                                |Features                                                                                                                                                           |QTY|Cost Per  [EUR]|Cost  [EUR]|
|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|---|---------------|-----------|
|M5 Rover C Pro                  |Programmable Mecanum wheel omnidirectional robot base. 4x N20 worm gear motors to drive the wheels directly by the motor driver. Servo gripping mechanism. |I2C Address 0x38, remote control, gripper Programmable, Four-channel motor driver, Extra Grove ports for expansion, STM32F030C6T6, I2C 16340(700mAh) battery holder|1  |60             |60         |
|Wemos Battery Shield            |18650 Battery Shield (V3) for Raspberry Pi & Arduino Cheap, portable power supply module.                                                                  |In: 5V/500mA (Micro USB) Out: 5VDC (USB type A) 3x 5VDC (up to 4A) + 3x 3VDC (up to 1A) Battery Charging /  Charged LEDs Overcharge, Deep Discharge Protection     |1  |2.5            |2.5        |
|18650 Li-Ion                    |Battery: Samsung Li-Ion 18650 cell                                                                                                                         |3.6V 2600mAh                                                                                                                                                       |1  |11             |11         |
|M5StickC ESP32                  |M5 Stick C is a mini M5 Stack, powered by ESP32.  It is a portable, easy-to-use, open source, IoT development board.                                       |ESP32-based, IMU, LED, IR, Mic,  3 buttons, LCD(0.96 in), battery Wearable / Wall mounted, support: UIFlow, MicroPython, Arduino, .NET nanoFramework               |2  |13.7           |27.4       |
|JoyC Omni-directional Controller|Rocker module for the M5 Stick C & Rover base.                                                                                                             |STM32F030F4, I2C, 12 RGB LEDs omni-directional movement & button press  16340 battery holder                                                                       |1  |18.2           |18.2       |
|Raspberry Pi Zero 1 W v1.3      |Flexible, compact Raspberry Pi Single Board Computer. Size: 65mm long by 30mm wide, affordable.                                                            |1GHz single-core CPU, 512MB RAM Mini HDMI port, Micro USB OTG port Micro USB power, HAT-compatible 40-pin header CSI camera connector WiFi (2.4GHz) & Bluetooth    |1  |13.7           |13.7       |
|Raspberry Pi Camera Board v2.1  |High quality camera based on Sony IMX219PQ image sensor. Supports FHD video and still photographs.                                                         |Fixed focus lens, 8 megapixel resolution  Support 1080p30, 720p60, 480p90 25mm x 23mm x 9mm, just over 3g; CSI connector                                           |1  |23.65          |23.65      |
|CSI Camera Ribbon Adapter       |Raspberry Pi Zero adapter cable to Camera CSI connector                                                                                                    |Length: 15 cm, CSI 22-pin (Pi Zero) to 15-pin (Camera board)                                                                                                       |1  |5.12           |5.12       |
|0.67x Wide Angle, Macro, Fisheye|Magnetic interlocking lens camera add-on kit                                                                                                               |Self-adhesive metal ring mount 0.67x wide angle, macro lens combo 180 deg field of view fisheye lens                                                               |1  |7              |7          |
|Totals                          |Listed Prices: April 2023                                                                                                                                  |Total Part Count:                                                                                                                                                  |10 |Total [EUR]:   |168.57     |
