import serial
import time
from typing import List, Optional, Tuple

class RoboticArmController:
    """
    4自由度机械臂控制器
    通过蓝牙与Arduino通信，控制机械臂运动
    """
    
    def __init__(self, bluetooth_port: str = 'COM9', baud_rate: int = 9600):
        """
        初始化机械臂控制器
        
        Args:
            bluetooth_port: 蓝牙串口号 (如 'COM9')
            baud_rate: 波特率，默认9600
        """
        self.bluetooth_port = bluetooth_port
        self.baud_rate = baud_rate
        self.serial_connection: Optional[serial.Serial] = None
        self.is_connected = False
        
    def connect(self) -> bool:
        """
        连接机械臂
        
        Returns:
            bool: 连接是否成功
        """
        try:
            print(f"正在连接 {self.bluetooth_port}...")
            self.serial_connection = serial.Serial(
                self.bluetooth_port, 
                self.baud_rate, 
                timeout=5
            )
            time.sleep(2)
            
            print("发送握手请求...")
            self.serial_connection.write(b'H')
            
            response = self.serial_connection.readline().decode().strip()
            if response == "连接成功":
                print("✓ 机械臂连接成功！")
                self.is_connected = True
                return True
            else:
                print(f"✗ 连接失败: {response}")
                self.disconnect()
                return False
                
        except serial.SerialException as e:
            print(f"✗ 连接失败: {e}")
            print("请检查:")
            print("1. 蓝牙是否已配对")
            print(f"2. 端口号 {self.bluetooth_port} 是否正确")
            print("3. 是否有其他程序占用了该端口")
            return False
        except Exception as e:
            print(f"✗ 连接错误: {e}")
            return False
    
    def disconnect(self) -> None:
        """断开机械臂连接"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.is_connected = False
            print("机械臂连接已关闭")
    
    def _send_command(self, command: str) -> Optional[str]:
        """
        发送命令并获取回复
        
        Args:
            command: 要发送的命令
            
        Returns:
            Optional[str]: 回复内容，失败返回None
        """
        if not self.is_connected or not self.serial_connection:
            print("✗ 机械臂未连接")
            return None
            
        try:
            self.serial_connection.write(command.encode())
            time.sleep(0.1)
            
            response = self.serial_connection.readline().decode().strip()
            return response if response else None
        except Exception as e:
            print(f"✗ 命令执行错误: {e}")
            return None
    
    def move_to(self, angles: List[int]) -> bool:
        """
        移动机械臂到指定角度
        
        Args:
            angles: 4个自由度的角度列表，每个角度范围0-180
            
        Returns:
            bool: 移动是否成功
        """
        if len(angles) != 4:
            print("✗ 错误: 必须提供4个角度值")
            return False
            
        # 验证角度范围
        for i, angle in enumerate(angles):
            if not 0 <= angle <= 180:
                print(f"✗ 错误: 第{i+1}个角度 {angle} 超出范围(0-180)")
                return False
        
        command = f"M:{','.join(map(str, angles))}\n"
        print(f"发送移动指令: {command.strip()}")
        
        response = self._send_command(command)
        if response and response.startswith("移动成功"):
            print(f"✓ {response}")
            return True
        else:
            print(f"✗ 移动失败: {response}")
            return False
    
    def get_status(self) -> Optional[dict]:
        """
        获取机械臂当前状态
        
        Returns:
            Optional[dict]: 状态字典，包含当前角度和位置信息
        """
        response = self._send_command("G\n")
        if response and response.startswith("状态:"):
            try:
                # 解析状态信息: 状态:x1,x2,x3,x4
                status_str = response.split(":", 1)[1]
                angles = list(map(int, status_str.split(",")))
                return {
                    "angles": angles,
                    "joints": {
                        "base": angles[0],
                        "shoulder": angles[1],
                        "elbow": angles[2],
                        "wrist": angles[3]
                    }
                }
            except (ValueError, IndexError):
                print(f"✗ 状态解析失败: {response}")
                return None
        else:
            print(f"✗ 获取状态失败: {response}")
            return None
    
    def stop(self) -> bool:
        """停止所有电机"""
        print("停止所有电机...")
        response = self._send_command("S\n")
        if response and response.startswith("已停止"):
            print(f"✓ {response}")
            return True
        else:
            print(f"✗ 停止失败: {response}")
            return False
    
    def go_home(self) -> bool:
        """回到初始位置"""
        print("回到初始位置...")
        response = self._send_command("HOME\n")
        if response and response.startswith("已回到初始位置"):
            print(f"✓ {response}")
            return True
        else:
            print(f"✗ 回到初始位置失败: {response}")
            return False
    
    def move_joint(self, joint_index: int, angle: int) -> bool:
        """
        移动单个关节
        
        Args:
            joint_index: 关节编号 (0-3)
            angle: 目标角度 (0-180)
            
        Returns:
            bool: 移动是否成功
        """
        if not 0 <= joint_index <= 3:
            print("✗ 错误: 关节编号必须是0-3")
            return False
            
        if not 0 <= angle <= 180:
            print("✗ 错误: 角度必须在0-180之间")
            return False
        
        # 获取当前状态
        status = self.get_status()
        if not status:
            return False
            
        angles = status["angles"]
        angles[joint_index] = angle
        
        return self.move_to(angles)
    
    def calibrate(self) -> bool:
        """校准机械臂"""
        print("校准机械臂...")
        response = self._send_command("CALIBRATE\n")
        if response and response.startswith("校准完成"):
            print(f"✓ {response}")
            return True
        else:
            print(f"✗ 校准失败: {response}")
            return False
    
    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.disconnect()


def test_basic_control():
    """测试基本控制功能"""
    print("=" * 50)
    print("机械臂基础控制测试")
    print("=" * 50)
    
    # 使用上下文管理器自动连接和断开
    with RoboticArmController() as arm:
        if not arm.is_connected:
            return
        
        # 测试获取状态
        print("\n1. 获取当前状态:")
        status = arm.get_status()
        if status:
            print(f"   当前角度: {status['angles']}")
            print(f"   基座: {status['joints']['base']}°")
            print(f"   肩部: {status['joints']['shoulder']}°")
            print(f"   肘部: {status['joints']['elbow']}°")
            print(f"   手腕: {status['joints']['wrist']}°")
        
        # 测试移动到新位置
        print("\n2. 移动到测试位置:")
        test_angles = [90, 90, 90, 90]
        success = arm.move_to(test_angles)
        
        if success:
            time.sleep(1)
            
            # 测试单关节控制
            print("\n3. 单关节测试:")
            arm.move_joint(0, 120)
            time.sleep(1)
            arm.move_joint(0, 60)
            time.sleep(1)
            
            # 测试回到初始位置
            print("\n4. 回到初始位置:")
            arm.go_home()
        
        # 测试停止
        print("\n5. 测试停止:")
        arm.stop()


def test_sequence():
    """测试序列控制"""
    print("\n" + "=" * 50)
    print("机械臂序列控制测试")
    print("=" * 50)
    
    with RoboticArmController() as arm:
        if not arm.is_connected:
            return
        
        # 定义序列动作
        sequences = [
            ([0, 0, 0, 0], "初始位置"),
            ([45, 45, 45, 45], "第一序列"),
            ([90, 90, 90, 90], "第二序列"),
            ([135, 135, 135, 135], "第三序列"),
            ([180, 180, 180, 180], "极限位置"),
            ([90, 90, 90, 90], "回到中心"),
            ([0, 0, 0, 0], "回到初始")
        ]
        
        for angles, description in sequences:
            print(f"\n执行: {description}")
            print(f"目标角度: {angles}")
            
            if arm.move_to(angles):
                time.sleep(2)
            else:
                print("移动失败，停止序列")
                break


if __name__ == "__main__":
    print("机械臂控制程序")
    print("选择测试模式:")
    print("1. 基础控制测试")
    print("2. 序列控制测试")
    
    try:
        choice = input("请输入选择 (1 或 2): ").strip()
        
        if choice == "1":
            test_basic_control()
        elif choice == "2":
            test_sequence()
        else:
            print("无效选择")
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序错误: {e}")