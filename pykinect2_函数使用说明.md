# PyKinect2 库函数使用说明

PyKinect2 是一个用于访问微软 Kinect v2 驱动程序的 Python 库。本文档介绍了该库的主要函数和使用方法。

## 库概述

PyKinect2 库提供了对 Kinect v2 设备的访问，包括：
- 颜色帧捕获
- 深度帧捕获
- 红外帧捕获
- 身体追踪
- 身体索引帧
- 音频数据

## 主要类和函数

### 1. PyKinectRuntime 类

这是库的核心类，用于管理 Kinect 设备并提供对各种帧的访问。

#### 初始化

```python
from pykinect2 import PyKinectRuntime
from pykinect2.PyKinectV2 import *

# 初始化 Kinect 运行时，指定要使用的帧源类型
kinect = PyKinectRuntime(FrameSourceTypes_Color | FrameSourceTypes_Depth | FrameSourceTypes_Body)
```

**帧源类型常量：**
- `FrameSourceTypes_None` (0) - 无帧源
- `FrameSourceTypes_Color` (1) - 颜色帧
- `FrameSourceTypes_Infrared` (2) - 红外帧
- `FrameSourceTypes_LongExposureInfrared` (4) - 长曝光红外帧
- `FrameSourceTypes_Depth` (8) - 深度帧
- `FrameSourceTypes_BodyIndex` (16) - 身体索引帧
- `FrameSourceTypes_Body` (32) - 身体帧
- `FrameSourceTypes_Audio` (64) - 音频帧

#### 资源管理

```python
# 使用上下文管理器（推荐）
with PyKinectRuntime(FrameSourceTypes_Color | FrameSourceTypes_Depth) as kinect:
    # 在这里使用 Kinect
    pass
# 自动关闭连接

# 或者手动关闭
kinect.close()
```

### 2. 帧获取方法

#### 检查新帧

```python
# 检查是否有新的帧
if kinect.has_new_color_frame():
    # 有新的颜色帧

if kinect.has_new_depth_frame():
    # 有新的深度帧

if kinect.has_new_body_frame():
    # 有新的身体帧

if kinect.has_new_body_index_frame():
    # 有新的身体索引帧

if kinect.has_new_infrared_frame():
    # 有新的红外帧

if kinect.has_new_long_exposure_infrared_frame():
    # 有新的长曝光红外帧

if kinect.has_new_audio_frame():
    # 有新的音频帧
```

#### 获取帧数据

```python
# 获取最新的颜色帧（返回 numpy 数组）
color_frame = kinect.get_last_color_frame()

# 获取最新的深度帧（返回 numpy 数组）
depth_frame = kinect.get_last_depth_frame()

# 获取最新的身体索引帧（返回 numpy 数组）
body_index_frame = kinect.get_last_body_index_frame()

# 获取最新的红外帧（返回 numpy 数组）
infrared_frame = kinect.get_last_infrared_frame()

# 获取最新的身体帧（返回身体数据）
body_frame = kinect.get_last_body_frame()
```

### 3. 身体追踪相关

#### 获取身体数据

```python
# 获取身体帧数据
body_frame = kinect.get_last_body_frame()

if body_frame is not None:
    # 遍历所有可能的身体
    for i in range(kinect.max_body_count):
        body = body_frame.bodies[i]
        if body.is_tracked:
            # 身体被追踪，可以获取关节信息
            joints = body.get_joints()
            
            # 获取特定关节
            head_joint = joints[PyKinectV2.JointType_Head]
            shoulder_left_joint = joints[PyKinectV2.JointType_ShoulderLeft]
```

#### 关节类型

身体追踪支持以下关节类型：
- `JointType_SpineBase` - 脊柱基部
- `JointType_SpineMid` - 脊柱中部
- `JointType_Neck` - 颈部
- `JointType_Head` - 头部
- `JointType_ShoulderLeft` - 左肩
- `JointType_ElbowLeft` - 左肘
- `JointType_WristLeft` - 左腕
- `JointType_HandLeft` - 左手
- `JointType_ShoulderRight` - 右肩
- `JointType_ElbowRight` - 右肘
- `JointType_WristRight` - 右腕
- `JointType_HandRight` - 右手
- `JointType_HipLeft` - 左髋
- `JointType_KneeLeft` - 左膝
- `JointType_AnkleLeft` - 左踝
- `JointType_FootLeft` - 左脚
- `JointType_HipRight` - 右髋
- `JointType_KneeRight` - 右膝
- `JointType_AnkleRight` - 右踝
- `JointType_FootRight` - 右脚

#### 坐标转换

```python
# 将身体关节位置转换为颜色空间坐标
color_point = kinect.body_joint_to_color_space(joint)

# 将身体关节位置转换为深度空间坐标
depth_point = kinect.body_joint_to_depth_space(joint)

# 批量转换关节坐标
color_points = kinect.body_joints_to_color_space(joints)
depth_points = kinect.body_joints_to_depth_space(joints)
```

### 4. 帧描述信息

```python
# 颜色帧描述
color_frame_desc = kinect.color_frame_desc
color_width = color_frame_desc.Width  # 通常为 1920
color_height = color_frame_desc.Height  # 通常为 1080

# 深度帧描述
depth_frame_desc = kinect.depth_frame_desc
depth_width = depth_frame_desc.Width  # 通常为 512
depth_height = depth_frame_desc.Height  # 通常为 424

# 红外帧描述
infrared_frame_desc = kinect.infrared_frame_desc
infrared_width = infrared_frame_desc.Width  # 通常为 512
infrared_height = infrared_frame_desc.Height  # 通常为 424

# 身体索引帧描述
body_index_frame_desc = kinect.body_index_frame_desc
body_index_width = body_index_frame_desc.Width  # 通常为 512
body_index_height = body_index_frame_desc.Height  # 通常为 424
```

### 5. 完整示例

```python
from pykinect2 import PyKinectRuntime
from pykinect2.PyKinectV2 import *
import numpy as np

# 初始化 Kinect
kinect = PyKinectRuntime(FrameSourceTypes_Color | FrameSourceTypes_Depth | FrameSourceTypes_Body)

try:
    while True:
        # 检查新帧
        if kinect.has_new_color_frame():
            color_frame = kinect.get_last_color_frame()
            # 处理颜色帧...
            
        if kinect.has_new_depth_frame():
            depth_frame = kinect.get_last_depth_frame()
            # 处理深度帧...
            
        if kinect.has_new_body_frame():
            body_frame = kinect.get_last_body_frame()
            if body_frame is not None:
                for i in range(kinect.max_body_count):
                    body = body_frame.bodies[i]
                    if body.is_tracked:
                        joints = body.get_joints()
                        # 获取关节坐标并转换到颜色空间
                        head = joints[JointType_Head]
                        color_point = kinect.body_joint_to_color_space(head)
                        # 使用坐标...
                        
except KeyboardInterrupt:
    print("程序结束")
finally:
    kinect.close()
```

## 注意事项

1. 确保 Kinect v2 设备已正确连接到计算机
2. 需要安装 Kinect for Windows SDK
3. 建议使用上下文管理器（with 语句）来确保资源正确释放
4. 帧数据返回为 numpy 数组，可以直接用于图像处理
5. 身体追踪需要足够的光照条件和空间

## 版本信息

- 库版本：2.0.0
- 作者：Microsoft Corporation and contributors
- 许可证：MIT