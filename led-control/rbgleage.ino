#include "FastLED.h" 
#include <SoftwareSerial.h> 

#define NUM_LEDS 144 //Number of leds in the strip, WS2812B
#define DATA_PIN 3 //Pin 3 of the arduino

CRGB leds[NUM_LEDS];

int goal;

void setup() {
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
  Serial.begin(9600); //set baud rate
  Serial.println("Connected!");
}

void loop() {
  while (Serial.available() > 0) {
    goal = Serial.parseInt();
    Serial.println(goal);
    if (goal > 0){
      Serial.println("Goal detected");
      photonsprayer();
      goal = 0;  
    }
  }
}

void photonsprayer(){
  Serial.println("RGB madness");
  for (int i = 0; i <= 25; i++) {
    static uint8_t hue = 0;
    for(int led = 0; led < 144; led++) { 
            leds[led] = CRGB::Blue; 
    }
    FastLED.show(); 
    delay(100);
    FastLED.showColor(CHSV(0, 0, 0));
  }
  FastLED.showColor(CHSV(0, 0, 0));
}
