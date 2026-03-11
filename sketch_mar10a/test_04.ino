#include <Servo.h>

// 1. 定义4个舵机对象（对应4自由度）
Servo baseServo;    // 轴1：底座旋转
Servo bigArmServo;  // 轴2：大臂升降
Servo smallArmServo;// 轴3：小臂屈伸（联动大臂）
Servo clawServo;    // 轴4：夹爪开合

const int servoPin1 = 8;  // 舵机信号引脚（固定，方便修改）
const int servoPin2 = 9;  // 舵机信号引脚（固定，方便修改）
const int servoPin3 = 10;  // 舵机信号引脚（固定，方便修改）
const int servoPin4 = 11;  // 舵机信号引脚（固定，方便修改）
const int delayTime = 20; // 每步延时（增大到20ms，确保舵机到位）

// 2. 核心参数（根据你的机械臂微调）
const int ANGLE_SUM = 110;    // 大臂+小臂角度和（夹爪水平的关键）
const int BASE_MIN = 30, BASE_MAX = 120;       // 小臂安全范围
const int BIG_ARM_MIN = 60, BIG_ARM_MAX = 150;  // 大臂安全范围
const int CLAW_CLOSE = 120, CLAW_OPEN = 45;     // 夹爪开合角度

// 3. 初始化角度（上电复位姿态）
int baseAngle = 90;    // 底座正前
int bigArmAngle = 100;  // 大臂初始位
int smallArmAngle = 60; // 小臂联动位
int clawAngle = CLAW_OPEN; // 夹爪初始张开

void setup() {
  // 绑定舵机引脚（根据你的实际接线修改！）
  baseServo.attach(servoPin1);
  bigArmServo.attach(servoPin2);
  smallArmServo.attach(servoPin3);
  clawServo.attach(servoPin4);

  baseServo.write(base);
  bigArmServo.write(bigArm);
  smallArmServo.write(smallArm);
  clawServo.write(claw);
  // 串口初始化（用于手动控制）
  //Serial.begin(9600);
 // Serial.println("4轴机械臂控制就绪！");
  //Serial.println("指令说明：");
  //Serial.println("w=大臂上升  s=大臂下降  a=底座左转  d=底座右转");
  //Serial.println("o=夹爪打开  c=夹爪闭合  r=复位初始姿态");

  // 上电复位到安全水平姿态
  delay(500); // MG90S到位延时
}

// 4. 核心联动函数：设置机械臂姿态（保证夹爪水平）
void setArmPose(int base, int bigArm, int claw) {
  // 安全限位（防止舵机堵转）
  base = constrain(base, BASE_MIN, BASE_MAX);
  bigArm = constrain(bigArm, BIG_ARM_MIN, BIG_ARM_MAX);
  claw = constrain(claw, CLAW_CLOSE, CLAW_OPEN);

  // 计算小臂联动角度（保证角度和不变，夹爪水平）
  //int smallArm = ANGLE_SUM - bigArm;

  // 执行舵机动作
  baseServo.write(base);
  bigArmServo.write(bigArm);
  smallArmServo.write(smallArm);
  clawServo.write(claw);

  // 更新全局角度（方便后续控制）
  baseAngle = base;
  bigArmAngle = bigArm;
  smallArmAngle = smallArm;
  clawAngle = claw;

  // 串口回显当前姿态（调试用）
  //Serial.print("当前姿态：底座=");
  //Serial.print(baseAngle);
  //Serial.print(" 大臂=");
  //Serial.print(bigArmAngle);
  //Serial.print(" 小臂=");
  //Serial.print(smallArmAngle);
  //Serial.print(" 夹爪=");
  //Serial.println(clawAngle);
}

void loop() {
  // 5. 串口指令控制（新手友好，直接发字母即可）
  if (Serial.available() > 0) {
    char cmd = Serial.read(); // 读取串口指令
    int step = 2; // 每次转动步长（MG90S设2°最稳）

    switch(cmd) {
      case 'w': // 大臂上升（夹爪水平抬高）
        setArmPose(baseAngle, bigArmAngle + step, clawAngle);
        break;
      case 's': // 大臂下降（夹爪水平降低）
        setArmPose(baseAngle, bigArmAngle - step, clawAngle);
        break;
      case 'a': // 底座左转
        setArmPose(baseAngle - step, bigArmAngle, clawAngle);
        break;
      case 'd': // 底座右转
        setArmPose(baseAngle + step, bigArmAngle, clawAngle);
        break;
      case 'o': // 夹爪打开
        setArmPose(baseAngle, bigArmAngle, CLAW_OPEN);
        break;
      case 'c': // 夹爪闭合
        setArmPose(baseAngle, bigArmAngle, CLAW_CLOSE);
        break;
      case 'r': // 复位初始姿态
        setArmPose(90, 50, CLAW_OPEN);
        break;
      default: // 未知指令提示
        Serial.println("未知指令！请发送 w/s/a/d/o/c/r");
        break;
    }
    delay(50); // 指令执行间隔，避免动作过快
  }
}
