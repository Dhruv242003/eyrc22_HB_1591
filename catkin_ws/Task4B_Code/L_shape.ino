
#include <AccelStepper.h>
#include <elapsedMillis.h>

const int dirPin1 = 8;
const int stepPin1 = 6;
const int dirPin2 = 12;
const int stepPin2 = 10;
const int dirPin3 = 45;
const int stepPin3 = 13;


AccelStepper StepperFront(AccelStepper::DRIVER, stepPin1, dirPin1);
AccelStepper StepperLeft(AccelStepper::DRIVER, stepPin2, dirPin2);
AccelStepper StepperRight(AccelStepper::DRIVER, stepPin3, dirPin3);

elapsedMillis timeSpent;

void setup() {
  Serial.begin(115200);

  StepperFront.setMaxSpeed(500.0);
  StepperRight.setMaxSpeed(500.0);
  StepperLeft.setMaxSpeed(500.0);
  StepperFront.setSpeed(160.0);
  StepperRight.setSpeed(160.0);
  StepperLeft.setSpeed(160.0);

}

void loop() {


  float vel_z, vel_x, vel_y;


  if (timeSpent < 2950) {
    BotIK(0.0 , 0.0 , 170.0 );
  }
  else if (timeSpent > 2950 && timeSpent < 3000) {
    BotIK(0.0 , 0.0 , 0.0 );
  }
  else if (timeSpent > 3000 && timeSpent < 5950) {
    BotIK(0.0 , 0.0 , -170.0 );
  }
  else if (timeSpent > 5950 && timeSpent < 6000) {
    BotIK(0.0 , 0.0 , 0.0 );
  }
  else if (timeSpent > 6000 && timeSpent < 8950) {
    BotIK(0.0 , -170.0 , 0.0 );
  }
  else if (timeSpent > 8950 && timeSpent < 9000) {
    BotIK(0.0 , 0.0 , 0.0 );
  }

  else if (timeSpent > 9000 && timeSpent < 12000) {
    BotIK(0.0 , 170.0 , 0.0 );
  }
  else {
    BotIK(0.0 , 0.0 , 0.0 );
  }
}

void BotIK(float vel_z, float vel_x, float vel_y) {


  float Vf, Vr, Vl;
  float d = 12;
  Vf = -vel_z * d + vel_x;

  Vr = -vel_z * d + (-0.5) * vel_x + (-0.8660) * vel_y;

  Vl = -vel_z * d + (-0.5) * vel_x + (0.8660) * vel_y;

  StepperFront.setSpeed(Vf);
  StepperRight.setSpeed(Vr);
  StepperLeft.setSpeed(Vl);

  StepperFront.runSpeed();
  StepperRight.runSpeed();
  StepperLeft.runSpeed();

}
