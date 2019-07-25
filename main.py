# -*- coding: utf-8 -*-
'''
Created on 04.07.2019

@author: yu03
'''

from pyueye_example_camera import Camera
from pyueye_example_utils import FrameThread
from pyueye_example_gui import PyuEyeQtApp, PyuEyeQtView
from PyQt5 import QtGui
from pyueye import ueye
import cv2
import numpy as np


def process_image(self, image_data):

    # reshape the image data as 1dimensional array
    image = image_data.as_1d_image()   
#     print(image) 
    
    # show the image with Qt
    return QtGui.QImage(image.data,
                        image_data.mem_info.width,
                        image_data.mem_info.height,
                        QtGui.QImage.Format_Grayscale8)

def main():

    # we need a QApplication, that runs our QT Gui Framework    
    app = PyuEyeQtApp()

    # a basic qt window
    view = PyuEyeQtView()
    view.show()
    view.user_callback = process_image

    # camera class to simplify uEye API access
    cam = Camera()
    cam.init()
    cam.set_colormode(ueye.IS_CM_MONO8)
#     print(ueye.IS_CM_BGR8_PACKED)
    cam.set_aoi(0,0, 1280, 1024)
    cam.alloc()
    cam.capture_video()

    # a thread that waits for new images and processes all connected views
    thread = FrameThread(cam, view)
    thread.start()

    # cleanup
    app.exit_connect(thread.stop)
    app.exec_()

    thread.stop()
    thread.join()

    cam.stop_video()
    cam.exit()

if __name__ == "__main__":
    main()