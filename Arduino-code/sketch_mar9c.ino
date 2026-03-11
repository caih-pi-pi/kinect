void setup() {
  // 初始化串口，波特率9600（电脑端需匹配此值）
  Serial.begin(9600);  
  // 串口就绪后发送欢迎信息
  Serial.println("=== Arduino串口通讯测试 ===");
  Serial.println("请在串口监视器输入任意数字，我会回显给你～");
}

void loop() {
  // 检查串口是否有数据可读取
  if (Serial.available() > 0) {
    // 读取串口接收到的一个字符
    uint8_t num = Serial.parseInt();  
    
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
}