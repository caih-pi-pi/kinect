#include <Servo.h>

Servo myservo;  
int pos = 0; 
uint8_t num =0;   
const int servoPin = 9;  // 舵机信号引脚（固定，方便修改）
const int delayTime = 20; // 每步延时（增大到20ms，确保舵机到位）

void setup() {
  myservo.attach(servoPin);  
  // 初始化舵机到0°，避免上电位置偏移
  myservo.write(0);
  delay(500); 
   // 初始化串口，波特率9600（电脑端需匹配此值）
  Serial.begin(9600);  
  // 串口就绪后发送欢迎信息
  Serial.println("=== Arduino串口通讯测试 ===");
  Serial.println("请在串口监视器输入任意数字，我会回显给你～");
}

void loop() {
  if (Serial.available() > 0) {
    // 读取串口接收到的一个字符
     num = Serial.parseInt(); 
     // 向串口发送回显信息（替换printf，兼容所有板型）
    Serial.print("你发送的数字是：");    // 打印字符串（不换行）
    Serial.println();                   // 仅换行
    Serial.print("ASCII码：");          // 打印"ASCII码："
    Serial.println(num);       // 打印字符的ASCII码 + 换行
    
    // 清空串口缓冲区（避免残留数据干扰）
    while (Serial.available() > 0) {
      Serial.read();
    }
  }
  delay(10); // 降低循环频率，减少资源占用 
    
  // 第一步：从0°缓慢转到180°（逐度递增，不跳步）
  for (pos = 0; pos <= num; pos += 1) { 
    myservo.write(pos);  
    delay(delayTime);     // 每步等20ms，让舵机完全到位
  }
  delay(1000); // 转到180°后停留1秒，方便观察

  // 第二步：从180°缓慢转回0°（核心：逐度递减，必加！）
  for (pos = num; pos >= 0; pos -= 1) { 
    myservo.write(pos);  
    delay(delayTime);     
  }
  delay(1000); // 转回0°后停留1秒，循环往复
}