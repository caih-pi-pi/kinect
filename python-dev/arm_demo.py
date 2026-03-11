#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机械臂高级控制示例程序
演示如何使用RoboticArmController类进行复杂的机械臂控制
"""

from main import RoboticArmController
import time
import json


def demo_pick_and_place():
    """演示抓取和放置动作"""
    print("\n" + "=" * 60)
    print("机械臂抓取和放置演示")
    print("=" * 60)
    
    with RoboticArmController() as arm:
        if not arm.is_connected:
            return
        
        # 1. 回到初始位置
        print("\n1. 回到初始位置")
        arm.go_home()
        time.sleep(2)
        
        # 2. 抓取位置 - 模拟物体位置
        print("\n2. 移动到抓取位置")
        pick_angles = [45, 60, 90, 90]
        if arm.move_to(pick_angles):
            print("   ✓ 已到达抓取位置")
            time.sleep(1)
            
            # 3. 模拟抓取 - 保持当前位置
            print("\n3. 模拟抓取物体")
            print("   ✓ 物体已抓取")
            time.sleep(1)
            
            # 4. 提升 - 肘部关节向上
            print("\n4. 提升物体")
            lift_angles = [45, 60, 120, 90]
            if arm.move_to(lift_angles):
                print("   ✓ 物体已提升")
                time.sleep(1)
            
            # 5. 移动到放置位置
            print("\n5. 移动到放置位置")
            place_angles = [135, 60, 120, 90]
            if arm.move_to(place_angles):
                print("   ✓ 已到达放置位置")
                time.sleep(1)
            
            # 6. 放置物体
            print("\n6. 放置物体")
            print("   ✓ 物体已放置")
            time.sleep(1)
            
            # 7. 放置后恢复 - 回到初始位置
            print("\n7. 回到初始位置")
            arm.go_home()
            time.sleep(2)
            
            print("\n✓ 抓取和放置演示完成")


def demo_wave_motion():
    """演示挥手动作"""
    print("\n" + "=" * 60)
    print("机械臂挥手动作演示")
    print("=" * 60)
    
    with RoboticArmController() as arm:
        if not arm.is_connected:
            return
        
        # 1. 回到初始位置
        print("\n1. 回到初始位置")
        arm.go_home()
        time.sleep(2)
        
        # 2. 挥手动作序列
        wave_sequence = [
            ([90, 90, 90, 90], 0.5),   # 初始
            ([90, 90, 90, 120], 0.3),  # 手腕向右
            ([90, 90, 90, 60], 0.3),   # 手腕向左
            ([90, 90, 90, 120], 0.3),  # 手腕向右
            ([90, 90, 90, 90], 0.5),   # 回到中心
            ([90, 90, 90, 120], 0.3),  # 手腕向右
            ([90, 90, 90, 60], 0.3),   # 手腕向左
            ([90, 90, 90, 90], 0.5),   # 回到中心
        ]
        
        print("\n2. 执行挥手动作")
        for i, (angles, delay) in enumerate(wave_sequence, 1):
            print(f"   执行动作 {i}: {angles}")
            if arm.move_to(angles):
                time.sleep(delay)
        
        print("\n✓ 挥手动作演示完成")


def demo_dance_motion():
    """演示舞蹈动作"""
    print("\n" + "=" * 60)
    print("机械臂舞蹈动作演示")
    print("=" * 60)
    
    with RoboticArmController() as arm:
        if not arm.is_connected:
            return
        
        # 1. 回到初始位置
        print("\n1. 回到初始位置")
        arm.go_home()
        time.sleep(2)
        
        # 2. 舞蹈动作序列
        dance_sequence = [
            # 基础动作
            ([90, 90, 90, 90], 1.0),
            ([90, 120, 90, 90], 0.5),
            ([90, 60, 90, 90], 0.5),
            ([90, 90, 90, 90], 0.5),
            
            # 手腕动作
            ([90, 90, 90, 120], 0.3),
            ([90, 90, 90, 60], 0.3),
            ([90, 90, 90, 120], 0.3),
            ([90, 90, 90, 60], 0.3),
            ([90, 90, 90, 90], 0.5),
            
            # 肩部动作
            ([90, 120, 90, 90], 0.5),
            ([90, 60, 90, 90], 0.5),
            ([90, 90, 90, 90], 0.5),
            
            # 肘部动作
            ([90, 90, 120, 90], 0.5),
            ([90, 90, 60, 90], 0.5),
            ([90, 90, 90, 90], 0.5),
            
            # 组合动作
            ([120, 120, 120, 120], 0.5),
            ([60, 60, 60, 60], 0.5),
            ([90, 90, 90, 90], 1.0),
        ]
        
        print("\n2. 执行舞蹈动作")
        for i, (angles, delay) in enumerate(dance_sequence, 1):
            print(f"   舞蹈动作 {i}: {angles}")
            if arm.move_to(angles):
                time.sleep(delay)
        
        print("\n✓ 舞蹈动作演示完成")


def demo_custom_sequence():
    """演示自定义动作序列"""
    print("\n" + "=" * 60)
    print("机械臂自定义动作序列演示")
    print("=" * 60)
    
    with RoboticArmController() as arm:
        if not arm.is_connected:
            return
        
        # 1. 回到初始位置
        print("\n1. 回到初始位置")
        arm.go_home()
        time.sleep(2)
        
        # 2. 自定义序列 - 可以根据实际机械臂结构调整
        custom_sequence = [
            # 起始位置
            ([90, 90, 90, 90], 1.0),
            
            # 第一部分：手臂展开
            ([45, 90, 90, 90], 0.8),
            ([45, 120, 90, 90], 0.6),
            ([45, 120, 120, 90], 0.6),
            ([45, 120, 120, 120], 0.6),
            
            # 第二部分：收回
            ([45, 120, 120, 60], 0.6),
            ([45, 120, 90, 60], 0.6),
            ([45, 90, 90, 60], 0.6),
            ([90, 90, 90, 60], 0.8),
            
            # 第三部分：旋转
            ([90, 90, 90, 180], 0.8),
            ([90, 90, 90, 0], 0.8),
            ([90, 90, 90, 90], 1.0),
            
            # 第四部分：测试极限位置
            ([0, 0, 0, 0], 1.0),
            ([180, 180, 180, 180], 1.0),
            
            # 回到中心
            ([90, 90, 90, 90], 1.5),
        ]
        
        print("\n2. 执行自定义动作序列")
        for i, (angles, delay) in enumerate(custom_sequence, 1):
            print(f"   自定义动作 {i}: {angles}")
            if arm.move_to(angles):
                time.sleep(delay)
        
        print("\n✓ 自定义动作序列演示完成")


def demo_interactive_control():
    """演示交互式控制"""
    print("\n" + "=" * 60)
    print("机械臂交互式控制演示")
    print("=" * 60)
    
    with RoboticArmController() as arm:
        if not arm.is_connected:
            return
        
        print("\n1. 回到初始位置")
        arm.go_home()
        time.sleep(2)
        
        print("\n2. 交互式控制模式")
        print("   输入角度值控制单个关节 (0-180)")
        print("   输入 's' 停止所有电机")
        print("   输入 'h' 回到初始位置")
        print("   输入 'q' 退出")
        
        while True:
            try:
                user_input = input("\n输入命令 (关节号,角度): ").strip().lower()
                
                if user_input == 'q':
                    print("退出交互模式")
                    break
                elif user_input == 's':
                    arm.stop()
                elif user_input == 'h':
                    arm.go_home()
                elif ',' in user_input:
                    parts = user_input.split(',')
                    if len(parts) == 2:
                        joint = int(parts[0])
                        angle = int(parts[1])
                        print(f"移动关节 {joint} 到 {angle}°")
                        if arm.move_joint(joint, angle):
                            time.sleep(0.5)
                        else:
                            print("移动失败")
                    else:
                        print("输入格式错误")
                else:
                    print("未知命令")
                    
            except KeyboardInterrupt:
                print("\n用户中断")
                break
            except ValueError:
                print("输入格式错误")
            except Exception as e:
                print(f"错误: {e}")
        
        print("\n✓ 交互式控制演示完成")


def main():
    """主菜单"""
    print("机械臂高级控制演示程序")
    print("=" * 60)
    print("选择演示模式:")
    print("1. 抓取和放置演示")
    print("2. 挥手动作演示")
    print("3. 舞蹈动作演示")
    print("4. 自定义动作序列演示")
    print("5. 交互式控制演示")
    print("6. 运行所有演示")
    print("0. 退出")
    
    try:
        choice = input("\n请输入选择 (0-6): ").strip()
        
        if choice == "0":
            print("程序退出")
        elif choice == "1":
            demo_pick_and_place()
        elif choice == "2":
            demo_wave_motion()
        elif choice == "3":
            demo_dance_motion()
        elif choice == "4":
            demo_custom_sequence()
        elif choice == "5":
            demo_interactive_control()
        elif choice == "6":
            print("\n开始运行所有演示...")
            demo_pick_and_place()
            time.sleep(2)
            demo_wave_motion()
            time.sleep(2)
            demo_dance_motion()
            time.sleep(2)
            demo_custom_sequence()
            time.sleep(2)
            print("\n✓ 所有演示完成")
        else:
            print("无效选择")
            
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序错误: {e}")


if __name__ == "__main__":
    main()