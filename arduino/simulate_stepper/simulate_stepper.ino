/* 
 *  simulate two stepper motors with LEDs blinking for each step & direction
 */
#define MOTOR_LEFT 0
#define MOTOR_RIGHT 1

#define DIRECTION_LEFT 0
#define DIRECTION_RIGHT 1

#define BAUDRATE 9600

int pins[2][2] = {
  {8, 9}, // left
  {11, 12}  // right
};

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(BAUDRATE);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  
  pinMode(pins[MOTOR_LEFT][DIRECTION_LEFT], OUTPUT);
  pinMode(pins[MOTOR_LEFT][DIRECTION_RIGHT], OUTPUT);
  pinMode(pins[MOTOR_RIGHT][DIRECTION_LEFT], OUTPUT);
  pinMode(pins[MOTOR_RIGHT][DIRECTION_RIGHT], OUTPUT);

  // Serial.println("Ready");
  Serial.write('A');
  Serial.flush();
}

void blink_all() { 
  digitalWrite(pins[MOTOR_LEFT][DIRECTION_LEFT], HIGH);    
  digitalWrite(pins[MOTOR_LEFT][DIRECTION_RIGHT], HIGH);   
  digitalWrite(pins[MOTOR_RIGHT][DIRECTION_LEFT], HIGH);    
  digitalWrite(pins[MOTOR_RIGHT][DIRECTION_RIGHT], HIGH);   
  delay(200);                 
  digitalWrite(pins[MOTOR_LEFT][DIRECTION_LEFT], LOW);    
  digitalWrite(pins[MOTOR_LEFT][DIRECTION_RIGHT], LOW);   
  digitalWrite(pins[MOTOR_RIGHT][DIRECTION_LEFT], LOW);    
  digitalWrite(pins[MOTOR_RIGHT][DIRECTION_RIGHT], LOW);   
  delay(200);                 
}

void blink(int pin) { 
  digitalWrite(pin, HIGH);    
  delay(5);                 
  digitalWrite(pin, LOW);     
}
  
void rotate(int motor, int dir) { 
  blink(pins[motor][dir]);
//  switch (motor) {
//    case MOTOR_LEFT:
//      Serial.print('L');
//      break;
//    case MOTOR_RIGHT:
//      Serial.print('R');
//      break;
//  }
//  switch (dir) {
//    case DIRECTION_LEFT:
//      Serial.print('l');
//      break;
//    case DIRECTION_RIGHT:
//      Serial.print('r');
//      break;
//  }
//  Serial.println(); 
}

char c;
// String s;

void loop() {
//  blink(pins[MOTOR_LEFT][DIRECTION_LEFT]);
//  blink(pins[MOTOR_LEFT][DIRECTION_RIGHT]);
//  blink(pins[MOTOR_RIGHT][DIRECTION_LEFT]);
//  blink(pins[MOTOR_RIGHT][DIRECTION_RIGHT]);
//  delay(2000);                       

//  rotate(MOTOR_LEFT, DIRECTION_LEFT);
//  rotate(MOTOR_LEFT, DIRECTION_RIGHT);    
//  rotate(MOTOR_RIGHT, DIRECTION_LEFT);
//  rotate(MOTOR_RIGHT, DIRECTION_RIGHT);    
//  delay(1000);     

  if (Serial.available() > 0) {
//    blink_all();
//    s = Serial.readString();
//    s.trim();
//    s.toLowerCase();
//    if (s == "ll") {
//      rotate(MOTOR_LEFT, DIRECTION_LEFT);
//    }
//    if (s == "lr") {
//      rotate(MOTOR_LEFT, DIRECTION_RIGHT);
//    }
//    if (s == "rl") {
//      rotate(MOTOR_RIGHT, DIRECTION_LEFT);
//    }
//    if (s == "rr") {
//      rotate(MOTOR_RIGHT, DIRECTION_RIGHT);
//    }
//    //delayMicroseconds(300); 
//    Serial.print(s);
//    Serial.flush();

//    blink_all();
    c = Serial.read();
    switch (c) {
      case 'a': rotate(MOTOR_LEFT, DIRECTION_LEFT); break;
      case 'b': rotate(MOTOR_LEFT, DIRECTION_RIGHT); break;
      case 'c': rotate(MOTOR_RIGHT, DIRECTION_LEFT); break;
      case 'd': rotate(MOTOR_RIGHT, DIRECTION_RIGHT); break;
    }
    Serial.write(c);
    Serial.flush();
  }
}
