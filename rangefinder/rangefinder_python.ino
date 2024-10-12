#define TRIG_PIN 9
#define ECHO_PIN 10

void setup() {
  // Start the serial communication to send data over USB
  Serial.begin(9600);
  
  // Configure the pins
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  // Send a 10 microsecond pulse to trigger the sensor
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Measure the duration of the pulse on the echo pin
  long duration = pulseIn(ECHO_PIN, HIGH);
  
  // Calculate the distance in centimeters (sound speed is 34300 cm/s)
  long distance = duration * 0.034 / 2;
  
  // Send the distance over serial
  Serial.println(distance);
  
  // Delay for a short time to avoid overwhelming the serial port
  delay(100);
}