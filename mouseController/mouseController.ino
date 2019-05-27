#include "Mouse.h"

// set pin numbers for switch, joystick axes, and LED:
const int switchPin = A3;      // switch to turn on and off mouse control
const int rightButton = A2;    // input pin for the mouse pushButton
const int leftButton = A4;    // input pin for the mouse pushButton
const int xAxis = A0;         // joystick X axis
const int yAxis = A1;         // joystick Y axis

// parameters for reading the joystick:
int range = 8;               // output range of X or Y movement
int responseDelay = 5;        // response delay of the mouse, in ms
int threshold = range / 16;    // resting threshold
int center = range / 2;       // resting position value

boolean mobile = false;

void setup() {
  // take control of the mouse:
//  Serial.begin(9600);
  Mouse.begin();
}

void loop() {
  // read and scale the two axes:
  int xReading = readAxis(A0);
  int yReading = readAxis(A1);
//  Serial.print(xReading);
//  Serial.print("\t");
//  Serial.println(yReading);


  if (digitalRead(switchPin)) {
    mobile = !mobile;
    delay(50);
  }
  
  mobile = mobile; 
  // if the mouse control state is active, move the mouse:
  if (mobile) {
    Mouse.move(xReading, yReading, 0);
  }

  handleButton(leftButton, MOUSE_LEFT);
  handleButton(rightButton, MOUSE_RIGHT);

  delay(responseDelay);
}


void handleButton(int mouseButton, int BUTTON) {
  // read the mouse button and click or not click:
  // if the mouse button is pressed:
  if (digitalRead(mouseButton) == HIGH) {
    // if the mouse is not pressed, press it:
    if (!Mouse.isPressed(BUTTON)) {
      Mouse.press(BUTTON);
    }
  }
  // else the mouse button is not pressed:
  else {
    // if the mouse is pressed, release it:
    if (Mouse.isPressed(BUTTON)) {
      Mouse.release(BUTTON);
    }
  }
}

static inline int8_t sgn(int val) {
 if (val < 0) return -1;
 if (val==0) return 0;
 return 1;
}

/*
  reads an axis (0 or 1 for x or y) and scales the
 analog input range to a range from 0 to <range>
 */
int readAxis(int thisAxis) {
  // read the analog input:
  float reading = analogRead(thisAxis);

  int resolution = 100;
  float bound = 2;
  float val = map(1023 - reading, 0, 1023, -resolution, resolution);
  return int(sgn(val) * sq(val/resolution) * 30);

//  // map the reading from the analog input range to the output range:
//  reading = map(1023 - reading, 0, 1023, 0, range);
//
//  // if the output reading is outside from the
//  // rest position threshold,  use it:
//  int distance = reading - center;
//
//  if (abs(distance) < threshold) {
//    distance = 0;
//  }
//
//  // return the distance for this axis:
//  return sgn(distance) * sq(distances);
}




