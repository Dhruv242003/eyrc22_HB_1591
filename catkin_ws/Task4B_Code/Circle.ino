
#include <AccelStepper.h>

float theta = 0;
void setupTimer1() {
  noInterrupts();

  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = 0;


  OCR1A = 31249;

  TCCR1B |= (1 << WGM12);

  TCCR1B |= (1 << CS11) | (1 << CS10);

  TIMSK1 |= (1 << OCIE1A);
  interrupts();
}
const int dirPin1 = 8;
const int stepPin1 = 6;
const int dirPin2 = 12;
const int stepPin2 = 10;
const int dirPin3 = 45;
const int stepPin3 = 13;


AccelStepper StepperFront(AccelStepper::DRIVER, stepPin1, dirPin1);
AccelStepper StepperLeft(AccelStepper::DRIVER, stepPin2, dirPin2);
AccelStepper StepperRight(AccelStepper::DRIVER, stepPin3, dirPin3);



void setup() {
  setupTimer1();
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

  float V = 200;

  vel_x = V * sin(theta);
  vel_y = V * cos(theta);


  BotIK(0.0 , vel_x , vel_y );




  if (theta > 6.24) {
    while (1) {
      BotIK(0.0 , 0 , 0 );
    }
  }
}



ISR(TIMER1_COMPA_vect) {
  theta += 0.03925;
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
