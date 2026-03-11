from .PyKinectRuntime import PyKinectRuntime, KinectBody, KinectBodyFrameData
from .PyKinectV2 import *

__version__ = '2.0.0'
__author__ = 'Microsoft Corporation and contributors'
__license__ = 'MIT'
__all__ = ['PyKinectRuntime', 'KinectBody', 'KinectBodyFrameData'] + PyKinectV2.__all__