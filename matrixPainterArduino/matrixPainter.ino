#include <Adafruit_NeoPixel.h>

#define LED_PIN PA8
#define WIDTH 16
#define HEIGHT 16
#define LED_COUNT (WIDTH * HEIGHT)

Adafruit_NeoPixel matrix(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

int XY(int x, int y) {
  if (y % 2 == 0)
    return y * WIDTH + x;
  else
    return y * WIDTH + (WIDTH - 1 - x);
}

void setup() {
  Serial.begin(9600);

  matrix.begin();
  matrix.clear();
  matrix.show();
}

void loop() {
  if (Serial.available()) {
    String message = Serial.readStringUntil('\n');

    if (message == "CLEAR") {
      matrix.clear();
      matrix.show();
      return;
    }
    
    if (message.startsWith("PX")) {
      int x, y, r, g, b;

      sscanf(
        message.c_str(),
        "PX,%d,%d,%d,%d,%d",
        &x, &y, &r, &g, &b);

      matrix.setPixelColor(
        XY(x, y),
        matrix.Color(r, g, b));

      matrix.show();
    }
  }
}