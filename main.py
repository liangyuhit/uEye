# -*- coding: utf-8 -*-
'''
Created on 04.07.2019

@author: yu03
'''

from pyueye_camera import Camera
from pyueye_utils import FrameThread
from pyueye_gui import PyuEyeQtApp, PyuEyeQtView
from PyQt5 import QtGui
from pyueye import ueye
import cv2
import numpy as np
import datetime



now = datetime.datetime.now()

file_name = 'test.npy'
f = open(file_name,'wb')
np.save(f, np.NaN)

# header = ['%s\n' %file_name,
#       'Local current time : %s\n' %now.strftime("%Y-%m-%d %H:%M:%S"),
#       '-------------------------------------------------\n',
#       ]
# 
# with open(file_name,'w') as fid:
#     fid.writelines(header)

def process_image(self, image_data):

    # reshape the image data as 1dimensional array
    image = image_data.as_1d_image()   
    print(image[0][:5])
    
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
    print('Color Mode:', cam.get_colormode())

#     print(ueye.IS_CM_BGR8_PACKED)
    cam.set_aoi(0, 0, 1280, 16)
    aoi = cam.get_aoi()
    print('AOI:', aoi.x, aoi.y, aoi.width, aoi.height)
    
    print('Framerate Range:', cam.get_FrameTimeRange()[0], cam.get_FrameTimeRange()[1],cam.get_FrameTimeRange()[2])
    
#     cam.set_fps(1/cam.get_FrameTimeRange()[0])
    cam.set_fps(1/cam.get_FrameTimeRange()[0])
    
    cam.set_exposure(0.1)
    print('Exposure Time:', cam.get_exposure())
    
#     print(cam.get_colordepth()[0], cam.get_colordepth()[1])
    cam.alloc()
    cam.capture_video()
    
    #a thread that waits for new images and processes all connected views
    thread = FrameThread(cam, view)
#     thread.setDaemon(True)
    thread.start()
    
    
    # cleanup
    app.exit_connect(thread.stop)
    app.exec_()
 
    print('Frame Rate:', cam.get_fps())
    thread.stop()
    thread.join()

    cam.stop_video()
    cam.exit()

if __name__ == "__main__":
    main()