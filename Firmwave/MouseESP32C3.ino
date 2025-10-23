#include "USB.h"
#include "USBHIDMouse.h"
#include <WiFi.h>
#include <WebServer.h>
#include "Config.h"

USBHIDMouse Mouse;
WebServer server(80);

String serialBuffer = "";

const char* WIFI_SSID_STA = "SUA_REDE_WIFI";   // Coloque aqui o Wi-Fi que sera usado 
const char* WIFI_PASS_STA = "SENHA_WIFI";

void sendLog(const String &msg) {
  Serial.println("[INFO] " + msg);
}

void sendError(const String &msg) {
  Serial.println("[ERROR] " + msg);
}

void setup() {
  Serial.begin(9600);
  Mouse.begin();
  USB.begin();

  pinMode(BTN_LEFT, INPUT_PULLUP);
  pinMode(BTN_RIGHT, INPUT_PULLUP);
  pinMode(BTN_SCROLL, INPUT_PULLUP);

  sendLog("Conectando ao Wi-Fi...");
  WiFi.begin(WIFI_SSID_STA, WIFI_PASS_STA);

  int timeout = 0;
  while (WiFi.status() != WL_CONNECTED && timeout < 20) {
    delay(500);
    Serial.print(".");
    timeout++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    IPAddress ip = WiFi.localIP();
    sendLog("Wi-Fi conectado com sucesso!");
    sendLog("IP: " + ip.toString());
  } else {
    sendError("Falha ao conectar no Wi-Fi. Verifique SSID/Senha.");
    sendError("O ESP32 entrará em modo Access Point como backup...");
    WiFi.softAP(WIFI_SSID, WIFI_PASS);
    IPAddress IP = WiFi.softAPIP();
    sendLog("Modo AP ativo. IP: " + IP.toString());
  }

  server.on("/command", HTTP_POST, handleWiFiCommand);
  server.begin();
  sendLog("Servidor HTTP iniciado!");
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
  if (body.length() == 0) {
    server.send(400, "text/plain", "Comando vazio");
    sendError("Comando Wi-Fi vazio recebido");
    return;
  }

  handleCommand(body);
  server.send(200, "text/plain", "Comando executado via Wi-Fi");
}

void handleCommand(String cmd) {
  cmd.trim();
  if (cmd.length() == 0) {
    sendError("Comando vazio recebido");
    return;
  }

  sendLog("Comando recebido: " + cmd);

  if (cmd.startsWith("MOUSE_MOVE:")) {
    int first = cmd.indexOf(':');
    int second = cmd.indexOf(':', first + 1);

    if (first == -1 || second == -1) {
      sendError("Formato inválido para MOUSE_MOVE");
      return;
    }

    int x = cmd.substring(first + 1, second).toInt();
    int y = cmd.substring(second + 1).toInt();
    Mouse.move(x, y);
    sendLog("Movimento executado (" + String(x) + ", " + String(y) + ")");

  } else if (cmd.startsWith("MOUSE_CLICK:")) {
    String btn = cmd.substring(cmd.indexOf(':') + 1);
    btn.trim();

    if (btn == "left") Mouse.click(MOUSE_LEFT);
    else if (btn == "right") Mouse.click(MOUSE_RIGHT);
    else if (btn == "middle") Mouse.click(MOUSE_MIDDLE);
    else sendError("Botão inválido: " + btn);

    sendLog("Clique executado: " + btn);

  } else if (cmd.startsWith("MOUSE_SCROLL:")) {
    int amount = cmd.substring(cmd.indexOf(':') + 1).toInt();
    Mouse.move(0, 0, amount);
    sendLog("Scroll executado (" + String(amount) + ")");

  } else {
    sendError("Comando desconhecido: " + cmd);
  }
}
