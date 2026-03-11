#include <Servo.h>

Servo myservo;  
int pos = 0;    
const int servoPin = 9;  // 舵机信号引脚（固定，方便修改）
const int delayTime = 20; // 每步延时（增大到20ms，确保舵机到位）

void setup() {
  myservo.attach(servoPin);  
  // 初始化舵机到0°，避免上电位置偏移
  myservo.write(100);
  delay(500); 
}

void loop() {
  
  delay(1000); // 转回0°后停留1秒，循环往复
}