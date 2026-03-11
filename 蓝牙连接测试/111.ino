#include <SoftwareSerial.h>

// 软串口设置：RX接D3 (蓝牙TX), TX接D2 (蓝牙RX)
SoftwareSerial BTSerial(3, 2); 
const int ledPin = 13; // 板载LED

void setup() {
  // 硬件串口用于调试（可选）
  Serial.begin(9600);
  // 蓝牙串口
  BTSerial.begin(9600);
  
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  
  Serial.println("等待蓝牙连接...");
}

void loop() {
  // 检查蓝牙是否有数据
  if (BTSerial.available()) {
    char c = BTSerial.read();
    
    // 如果收到 'H'（代表握手请求）
    if (c == 'H') {
      Serial.println("收到连接请求");
      
      // 闪灯3次表示收到连接
      for (int i = 0; i < 3; i++) {
        digitalWrite(ledPin, HIGH);
        delay(200);
        digitalWrite(ledPin, LOW);
        delay(200);
      }
      
      // 发送成功消息给Python
      BTSerial.println("连接成功");
      Serial.println("已发送'连接成功'");
    }
  }
}