# ArUco Marker Tracker with Pan-Tilt Servo Control

This project uses **OpenCV** and **ArUco markers** to detect a marker in real-time from a webcam, smoothly track its center, and control a 2-axis pan-tilt servo mechanism via an **ESP32** over serial communication.

The camera follows the marker by mapping its position in the frame to servo angles (0–180°), with smoothing and deadband to prevent jitter and unnecessary movements.

## Features

- Real-time ArUco marker detection using OpenCV
- Smooth servo movement with exponential smoothing
- Minimal serial commands only when position changes significantly
- Visual feedback: marker outline, center, crosshair, connecting line
- Easy calibration (invert axes by uncommenting one line)
- Works with standard hobby servos (SG90, MG996R, etc.)

## Hardware Requirements

- ESP32 (or any Arduino-compatible board with two PWM pins)
- 2x hobby servo motors (pan + tilt)
- USB webcam or ESP32-CAM (if using index 0/1 accordingly)
- Pan-tilt bracket/mechanism
- Power supply for servos (5–6V recommended, separate from ESP32 if high torque)

## Wiring

| Servo   | ESP32 Pin |
|---------|-----------|
| Pan (X) | GPIO 13   |
| Tilt (Y)| GPIO 12   |
| Signal wires → above pins<br>Power → external 5V + GND (common ground with ESP32!)**

> **Important**: Always share GND between ESP32 and servo power supply.

## Software Requirements

### Python (Host PC)
- Python 3.7+
- OpenCV: `pip install opencv-python`
- PySerial: `pip install pyserial`
- NumPy (installed with OpenCV)

### ESP32 (Arduino IDE or PlatformIO)
- Install **ESP32Servo** library by Kevin Harrington  
  → Arduino Library Manager → Search "ESP32Servo"\

  
https://www.youtube.com/watch?v=8GhdAhkSSAo

