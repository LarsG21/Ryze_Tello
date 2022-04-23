
## Description
In this Project, I programmed a drone ("Ryze Tello") to track a person and detect commands by hand-tracking.\
The main file is FaceTracking.py

## Setup
First, you need to start the drone and connect to its Wi-Fi. Then you start FaceTracking.py.\
You may first test the connection with Keyboard_Control.py you can now fly the drone using WASD for forward, left, back, right and Q,E for rotation counterclockwise and clockwise.\
The drone will print the current temperature and battery percentage if you connected successfully.\
Press "t" for takeoff and "l" for landing.

## Control
The drone detects the face and follows you and keeps a constant distance.\
On the screen you can see a box around your had id the tracking is successful.\
You now can hold Your hand in the box near your head to give the drone different commands.

## Commands:
All Fingers up means --> "Landing"\
Index finger up --> "Wait at current position"\
Index + Middle --> "Back to tracking mode"\
Index + Middle + Ring --> "360° turn"
