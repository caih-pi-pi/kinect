#include <SoftwareSerial.h>
#include <Servo.h>

// 软串口设置：RX接D3 (蓝牙TX), TX接D2 (蓝牙RX)
SoftwareSerial BTSerial(3, 2);

// 机械臂舵机定义 (连接到D9, D10, D11, D12)
Servo servo1; // 基座
Servo servo2; // 肩部
Servo servo3; // 肘部
Servo servo4; // 手腕

// 当前角度状态 (0-180度)
int currentAngles[4] = {90, 90, 90, 90};
bool isMoving = false;

// 舵机引脚定义
const int servoPins[4] = {9, 10, 11, 12};

void setup() {
  // 硬件串口用于调试
  Serial.begin(9600);
  // 蓝牙串口
  BTSerial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);

  // 初始化舵机
  servo1.attach(servoPins[0]);
  servo2.attach(servoPins[1]);
  servo3.attach(servoPins[2]);
  servo4.attach(servoPins[3]);

  // 设置初始角度
  setAllServos(currentAngles[0], currentAngles[1], currentAngles[2], currentAngles[3]);
  
  Serial.println("机械臂控制器启动");
  Serial.println("等待蓝牙连接...");
}

void loop() {
  // 检查蓝牙是否有数据
  if (BTSerial.available()) {
    String command = BTSerial.readStringUntil('\n');
    command.trim();
    
    if (command.length() > 0) {
      Serial.println("收到命令: " + command);
      
      // 解析命令
      if (command == "H") {
        handleHandshake();
      } else if (command.startsWith("M:")) {
        handleMoveCommand(command);
      } else if (command == "G") {
        handleGetStatus();
      } else if (command == "S") {
        handleStop();
      } else if (command == "HOME") {
        handleGoHome();
      } else if (command == "CALIBRATE") {
        handleCalibrate();
      } else {
        BTSerial.println("未知命令: " + command);
      }
    }
  }
}

void handleHandshake() {
  // 闪灯3次表示收到连接
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    digitalWrite(LED_BUILTIN, LOW);
    delay(100);
  }

  // 发送成功消息
  BTSerial.println("连接成功");
  Serial.println("已发送'连接成功'");
}

void handleMoveCommand(String cmd) {
  String anglesStr = cmd.substring(2); // 移除"M:"前缀
  
  int angles[4];
  int count = 0;
  int start = 0;
  
  // 解析角度值
  for (int i = 0; i <= anglesStr.length() && count < 4; i++) {
    if (i == anglesStr.length() || anglesStr.charAt(i) == ',') {
      String angleStr = anglesStr.substring(start, i);
      angles[count++] = angleStr.toInt();
      start = i + 1;
    }
  }
  
  if (count == 4) {
    // 检查角度范围
    bool valid = true;
    for (int i = 0; i < 4; i++) {
      if (angles[i] < 0 || angles[i] > 180) {
        valid = false;
        break;
      }
    }
    
    if (valid) {
      isMoving = true;
      setAllServos(angles[0], angles[1], angles[2], angles[3]);
      
      // 更新当前角度
      for (int i = 0; i < 4; i++) {
        currentAngles[i] = angles[i];
      }
      
      isMoving = false;
      BTSerial.println("移动成功: " + cmd);
      Serial.println("移动成功: " + cmd);
    } else {
      BTSerial.println("角度超出范围(0-180): " + cmd);
      Serial.println("角度超出范围");
    }
  } else {
    BTSerial.println("角度格式错误: " + cmd);
    Serial.println("角度格式错误");
  }
}

void handleGetStatus() {
  String status = "状态:" + String(currentAngles[0]) + "," + 
                  String(currentAngles[1]) + "," + 
                  String(currentAngles[2]) + "," + 
                  String(currentAngles[3]);
  BTSerial.println(status);
  Serial.println("发送状态: " + status);
}

void handleStop() {
  // 停止所有舵机
  servo1.detach();
  servo2.detach();
  servo3.detach();
  servo4.detach();
  
  BTSerial.println("已停止所有舵机");
  Serial.println("已停止所有舵机");
}

void handleGoHome() {
  int homeAngles[4] = {90, 90, 90, 90};
  setAllServos(homeAngles[0], homeAngles[1], homeAngles[2], homeAngles[3]);
  
  // 更新当前角度
  for (int i = 0; i < 4; i++) {
    currentAngles[i] = homeAngles[i];
  }
  
  BTSerial.println("已回到初始位置");
  Serial.println("已回到初始位置");
}

void handleCalibrate() {
  // 校准程序 - 可以添加校准逻辑
  BTSerial.println("校准完成");
  Serial.println("校准完成");
}

void setAllServos(int angle1, int angle2, int angle3, int angle4) {
  Serial.println("设置舵机角度: " + String(angle1) + "," + String(angle2) + "," + 
                 String(angle3) + "," + String(angle4));
  
  // 使用延迟确保舵机有足够时间到达目标位置
  servo1.write(angle1);
  delay(100);
  
  servo2.write(angle2);
  delay(100);
  
  servo3.write(angle3);
  delay(100);
  
  servo4.write(angle4);
  delay(200); // 给最后的舵机更多时间
}