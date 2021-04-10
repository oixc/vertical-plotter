/*Example sketch to control a stepper motor with A4988 stepper motor driver and Arduino without a library. More info: https://www.makerguides.com */

// Define stepper motor connections and steps per revolution:
#define RightDirPin 5
#define RightStepPin 2
#define LeftDirPin 6
#define LeftStepPin 3
#define stepsPerRevolution 200

void setup() {
  // Declare pins as output:
  pinMode(RightStepPin, OUTPUT);
  pinMode(RightDirPin, OUTPUT);
  pinMode(LeftStepPin, OUTPUT);
  pinMode(LeftDirPin, OUTPUT);
}

void loop() {
  // Set the spinning direction clockwise:
  digitalWrite(RightDirPin, HIGH);
  digitalWrite(LeftDirPin, HIGH);

  // Spin the stepper motor 1 revolution slowly:
  for (int i = 0; i < stepsPerRevolution; i++) {
    // These four lines result in 1 step:
    digitalWrite(LeftStepPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(LeftStepPin, LOW);
    delayMicroseconds(1000);
  }

  delay(1000);

  // Spin the stepper motor 1 revolution slowly:
  for (int i = 0; i < stepsPerRevolution * 2; i++) {
    // These four lines result in 1 step:
    digitalWrite(RightStepPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(RightStepPin, LOW);
    delayMicroseconds(1000);
  }

  delay(1000);

  // Set the spinning direction counterclockwise:
  digitalWrite(RightDirPin, LOW);
  digitalWrite(LeftDirPin, LOW);

  // Spin the stepper motor 1 revolution slowly:
  for (int i = 0; i < stepsPerRevolution*10; i++) {
    // These four lines result in 1 step:
    digitalWrite(RightStepPin, HIGH);
    digitalWrite(LeftStepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(RightStepPin, LOW);
    digitalWrite(LeftStepPin, LOW);
    delayMicroseconds(500);
  }

  delay(1000);
  
}
