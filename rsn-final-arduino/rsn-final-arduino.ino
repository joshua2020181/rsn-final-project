#include <SparkFun_TB6612.h>

const int PAN_PWM = 11;
const int PAN_IN_1 = 13;
const int PAN_IN_2 = 12;

const int TILT_PWM = 10;
const int TILT_IN_1 = 9;
const int TILT_IN_2 = 8;

const int STANDBY = 7;

const int DEFAULT_DURATION = 250;

Motor pan = Motor(PAN_IN_1, PAN_IN_2, PAN_PWM, 1, STANDBY);
Motor tilt = Motor(TILT_IN_1, TILT_IN_2, TILT_PWM, 1, STANDBY);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(PAN_IN_1, OUTPUT);
  pinMode(PAN_IN_2, OUTPUT);
  pinMode(TILT_IN_1, OUTPUT);
  pinMode(TILT_IN_2, OUTPUT);
}

bool isValid(int val) {
  return val >= -255 && val <= 255;
}

String readLastString() {
  String s = "";
  while (Serial.available() > 0) {
    s = Serial.readStringUntil('\n');
  }
  return s;
}

void loop() {
  if (Serial.available() > 0) {
    String input = readLastString();
    int separatorIndex = input.indexOf(';');
    if (separatorIndex != -1) {
      int pos1 = input.substring(0, separatorIndex).toInt();
      int pos2 = input.substring(separatorIndex + 1).toInt();
      Serial.println("pos1: " + String(pos1) + " pos 2: " + String(pos2));

      if (!isValid(pos1) || !isValid(pos2)) {
        Serial.println("Error");
      } else {
        pan.drive(pos1, DEFAULT_DURATION);
        tilt.drive(pos2, DEFAULT_DURATION);
      }
    }
  }
}
