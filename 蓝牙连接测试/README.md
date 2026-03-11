### 蓝牙测试用

蓝牙的链接参考https://tieba.baidu.com/p/4330334488

运行python西安板子发送“H”

```python

ser.write(b'H')

```

板子接受到后返回“连接成功”并闪灯，
```ino
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
```

python接受到后打印“✓ 蓝牙连接测试成功！”
```python
    print("等待回复...")
    response = ser.readline().decode().strip()
    
    if response:
        print(f"收到: {response}")
        if response == "连接成功":
            print("✓ 蓝牙连接测试成功！")
    else:
        print("✗ 没有收到回复")
```