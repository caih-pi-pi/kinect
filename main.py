import cv2
from pykinect2 import PyKinectRuntime, PyKinectV2
import numpy as np

# 初始化 Kinect
kinect = PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)

# 创建窗口
cv2.namedWindow('Kinect Color')
cv2.namedWindow('Kinect Depth')

while True:
    # 检查新帧
    if kinect.has_new_color_frame():
        color_frame = kinect.get_last_color_frame()
        # 重塑为图像尺寸
        color_frame = color_frame.reshape((480, 640, 4))[:, :, :3]  # 取 RGB 通道
        cv2.imshow('Kinect Color', color_frame)
    
    if kinect.has_new_depth_frame():
        depth_frame = kinect.get_last_depth_frame()
        # 重塑为图像尺寸
        depth_frame = depth_frame.reshape((480, 640))
        # 归一化深度值到 0-255
        depth_frame = (depth_frame / np.max(depth_frame) * 255).astype(np.uint8)
        cv2.imshow('Kinect Depth', depth_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 清理
kinect.close()
cv2.destroyAllWindows()