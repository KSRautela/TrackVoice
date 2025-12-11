#include <ESP32Servo.h>

Servo servoX;
Servo servoY;

int angleX = 90;
int angleY = 90;

void setup() {
  Serial.begin(115200);
  servoX.setPeriodHertz(50);
  servoY.setPeriodHertz(50);

  servoX.attach(13);  // pan
  servoY.attach(12);  // tilt

  servoX.write(angleX);
  servoY.write(angleY);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();  // remove \r or whitespace

    // Example: "X-2 Y3"
    int xIndex = cmd.indexOf('X');
    int yIndex = cmd.indexOf('Y');

    if (xIndex != -1) {
      int spaceIndex = cmd.indexOf(' ', xIndex);
      String xValStr = (spaceIndex != -1) ?
                        cmd.substring(xIndex + 1, spaceIndex) :
                        cmd.substring(xIndex + 1);
      int dx = xValStr.toInt();
      angleX = constrain(angleX + dx, 0, 180);
      servoX.write(angleX);
    }

    if (yIndex != -1) {
      String yValStr = cmd.substring(yIndex + 1);
      int dy = yValStr.toInt();
      angleY = constrain(angleY + dy, 0, 180);
      servoY.write(angleY);
    }
  }
}
