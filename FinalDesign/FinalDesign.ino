#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Alisia";  // WiFi SSID
const char* password = "iamgreat2104";  // WiFi Password
const char* serverUrl = "http://172.20.10.3:5001/api/vote";  // Flask API URL

const int buttonPin = 25;  // First button (Got it)
const int buttonPin2 = 26; // Second button (Confused)
const int buttonPin3 = 27; // Third button (Example Needed)
const int buttonPin4 = 13; // Fourth button (Undo)

void setup() {
    pinMode(buttonPin, INPUT_PULLDOWN);
    pinMode(buttonPin2, INPUT_PULLDOWN);
    pinMode(buttonPin3, INPUT_PULLDOWN);
    pinMode(buttonPin4, INPUT_PULLDOWN);
    Serial.begin(115200);

    // Connect to WiFi
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi...");
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }
    Serial.println("\nWiFi Connected!");
}

// Function to send HTTP POST request to Flask API
void sendVote(const char* vote) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(serverUrl);
        http.addHeader("Content-Type", "application/json");

        // Create JSON payload
        String payload = "{\"student_id\":\"esp32_1\",\"vote\":\"" + String(vote) + "\"}";
        int httpResponseCode = http.POST(payload);

        Serial.print("HTTP Response Code: ");
        Serial.println(httpResponseCode);

        http.end();
    } else {
        Serial.println("WiFi Disconnected - Cannot send vote");
    }
}

void loop() {
    // Read button states
    if (digitalRead(buttonPin) == HIGH) {
        Serial.println("Button 1 Pressed - 'got it'");
        sendVote("got it");
        delay(500);  // Debounce delay
    }

    if (digitalRead(buttonPin2) == HIGH) {
        Serial.println("Button 2 Pressed - 'confused'");
        sendVote("confused");
        delay(500);
    }

    if (digitalRead(buttonPin3) == HIGH) {
        Serial.println("Button 3 Pressed - 'example needed'");
        sendVote("example needed");
        delay(500);
    }

    if (digitalRead(buttonPin4) == HIGH) {
        Serial.println("Button 4 Pressed - 'undo'");
        sendVote("undo");
        delay(500);
    }
}