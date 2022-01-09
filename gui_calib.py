from __future__ import print_function
from __future__ import division
import cv2
import numpy as np
import argparse
np.set_printoptions(suppress=True)

class Fisheye:
    def __init__(self):
        self.WINDOW_NAME = 'cam calib'

    def get_track_vals(self):
        WINDOW_NAME = self.WINDOW_NAME
        fx = cv2.getTrackbarPos("fx",WINDOW_NAME)-1000
        fy = cv2.getTrackbarPos("fy",WINDOW_NAME)-1000
        cx = cv2.getTrackbarPos("cx",WINDOW_NAME)-1000
        cy = cv2.getTrackbarPos("cy",WINDOW_NAME)-1000
        k1 = (cv2.getTrackbarPos("k1",WINDOW_NAME)-1000)/1000
        k2 = (cv2.getTrackbarPos("k2",WINDOW_NAME)-1000)/1000
        p1 = (cv2.getTrackbarPos("p1",WINDOW_NAME)-1000)/1000
        p2 = (cv2.getTrackbarPos("p2",WINDOW_NAME)-1000)/100000
        k3 = (cv2.getTrackbarPos("k3",WINDOW_NAME)-1000)/10000
        mtx = np.array(
                        [[fx   ,  0.,  cx],
                         [  0. ,  fy,  cy],
                         [  0. ,  0.,  1.]])   
        dist = np.array([[k1, k2, p1, p2, k3]])
        return mtx, dist   

    def on_trackbar(self,val):
        mtx, dist = self.get_track_vals()
        self.dst = cv2.undistort(img, mtx, dist, None, None)
        cv2.imshow(self.WINDOW_NAME, self.dst)
        

    def fisheye_gui(self,img):
        """GUI for fishe eye correction
        Returns camera matrix and distortion coeffs
        """
        try:
            mtx = np.load('mtx.npy')
            dist = np.load('dist.npy')
        except:
            mtx = np.array(
                            [[763.06533889,   0.  ,       320.42956613],
                             [  0. ,        765.66818696, 267.88565043],
                             [  0. ,          0.   ,        1.        ]])               
            dist = np.array([[-0.06176994, -0.24929249,  0.00397634,  0.00001499,  1.75442713]])
            
            np.save('mtx.npy',mtx)
            np.save('dist.npy',dist)
            print('mtx0',mtx)
            print('dist0',dist)
        
        [[fx   ,  a,  cx],
         [  a ,  fy,  cy],
         [  a ,  a,  a]] = mtx
         
        [[k1, k2, p1, p2, k3]] = dist
        #import pdb;pdb.set_trace()
        WINDOW_NAME = self.WINDOW_NAME
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(WINDOW_NAME, 1000, 1000)
        cb = self.on_trackbar
        cv2.createTrackbar("fx",WINDOW_NAME,int(1000+fx)               ,3000, cb)
        cv2.createTrackbar("fy",WINDOW_NAME,int(1000+fy)               ,3000,cb)
        cv2.createTrackbar("cx",WINDOW_NAME,int(1000+cx)               ,3000,cb)
        cv2.createTrackbar("cy",WINDOW_NAME,int(1000+cy)               ,3000,cb)
        cv2.createTrackbar("k1",WINDOW_NAME,int(1000+k1*1000)          ,2000,cb)
        cv2.createTrackbar("k2",WINDOW_NAME,int(1000+k2*1000)          ,2000,cb)
        cv2.createTrackbar("p1",WINDOW_NAME,int(1000+p1*1000)          ,2000,cb)
        cv2.createTrackbar("p2",WINDOW_NAME,int(1000+p2*100000)        ,2000,cb)
        cv2.createTrackbar("k3",WINDOW_NAME,int(1000+k3 )              ,2000,cb)

        # Show some stuff
        self.on_trackbar(0)
        # Wait until user press some key
        print('press s to save')
        k = cv2.waitKey()
        
        if k==ord('s'): #press s to save
            mtx, dist = self.get_track_vals()
            print('\nmtx:\n',mtx)
            print('\ndist:\n',dist)
            np.save('mtx.npy',mtx)
            np.save('dist.npy',dist,'\n')
            cv2.imwrite('corrected.png', self.dst)
        
        return mtx, dist

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, default='cam1_images/0.jpg', help='input image path')
    args = parser.parse_args()
    print(args)
    
    fisheye = Fisheye()
    
    img = cv2.imread(args.path,1)
    fisheye.fisheye_gui(img)
    
    


        
    
