#include "USB.h"
#include "USBHIDMouse.h"
#include <WiFi.h>
#include <WebServer.h>
#include "config.h"

USBHIDMouse Mouse;
WebServer server(80);

String serialBuffer = "";

void setup() {
  Serial.begin(9600);
  Mouse.begin();
  USB.begin();

  pinMode(BTN_LEFT, INPUT_PULLUP);
  pinMode(BTN_RIGHT, INPUT_PULLUP);
  pinMode(BTN_SCROLL, INPUT_PULLUP);

  WiFi.softAP(WIFI_SSID, WIFI_PASS);
  IPAddress IP = WiFi.softAPIP();
  Serial.println("Wi-Fi ativo!");
  Serial.print("IP: ");
  Serial.println(IP);

  server.on("/command", HTTP_POST, handleWiFiCommand);
  server.begin();

  Serial.println("ESP32-C3 HID Mouse pronta!");
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      handleCommand(serialBuffer);
      serialBuffer = "";
    } else {
      serialBuffer += c;
    }
  }

  server.handleClient();

  if (digitalRead(BTN_LEFT) == LOW) {
    Mouse.click(MOUSE_LEFT);
    delay(150);
  }
  if (digitalRead(BTN_RIGHT) == LOW) {
    Mouse.click(MOUSE_RIGHT);
    delay(150);
  }
  if (digitalRead(BTN_SCROLL) == LOW) {
    Mouse.move(0, 0, 3);
    delay(150);
  }

  int xVal = analogRead(JOY_X);
  int yVal = analogRead(JOY_Y);

  if (abs(xVal - 2048) > JOY_DEADZONE || abs(yVal - 2048) > JOY_DEADZONE) {
    int dx = map(xVal, 0, 4095, -MOUSE_SPEED, MOUSE_SPEED);
    int dy = map(yVal, 0, 4095, MOUSE_SPEED, -MOUSE_SPEED);
    Mouse.move(dx, dy);
  }

  delay(20);
}

void handleWiFiCommand() {
  String body = server.arg("plain");
  handleCommand(body);
  server.send(200, "text/plain", "Comando executado via Wi-Fi");
}

void handleCommand(String cmd) {
  cmd.trim();

  if (cmd.startsWith("MOUSE_MOVE:")) {
    int first = cmd.indexOf(':');
    int second = cmd.indexOf(':', first + 1);
    int x = cmd.substring(first + 1, second).toInt();
    int y = cmd.substring(second + 1).toInt();
    Mouse.move(x, y);
    Serial.println("Movimento executado");

  } else if (cmd.startsWith("MOUSE_CLICK:")) {
    String btn = cmd.substring(cmd.indexOf(':') + 1);
    btn.trim();
    if (btn == "left") Mouse.click(MOUSE_LEFT);
    else if (btn == "right") Mouse.click(MOUSE_RIGHT);
    else if (btn == "middle") Mouse.click(MOUSE_MIDDLE);
    Serial.println("Clique executado");

  } else if (cmd.startsWith("MOUSE_SCROLL:")) {
    int amount = cmd.substring(cmd.indexOf(':') + 1).toInt();
    Mouse.move(0, 0, amount);
    Serial.println("Scroll executado");
  }
}
