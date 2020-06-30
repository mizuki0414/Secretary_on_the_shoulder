#define L_LED 13

unsigned long t0, t1;

void setup() {
  // open serial communications and wait for port to open:
  Serial.begin(57600);
  // initialize digital pin 13 as an output.
  pinMode(L_LED, OUTPUT);  
  digitalWrite(L_LED, HIGH);   // turn the LED on (HIGH is the voltage level)  
  t0 = millis();  
}

void loop() {   
  if (Serial.available()) {
    char c = Serial.read();   
    Serial.print(c);
  }
  t1 = millis();
  if ((t1 - t0)> 1000) {;
    t0 = t1;
    digitalWrite(L_LED, not digitalRead(L_LED));
  }
}
