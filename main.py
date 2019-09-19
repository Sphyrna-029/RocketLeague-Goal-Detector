import cv2
import numpy as np
from PIL import Image
from PIL import ImageGrab
from skimage.measure import compare_ssim


#~~~~~~~~~~~~~~~~~~CONFIG~~~~~~~~~~~~~~~~~~
#Area to capture. In this case our score will always be on the left hand side. This will be different depending on your game resolution.
#Top left corner
x = 795
y = 40
#Top right
x2 = 860
y2 = 100
#Angle
angle = -5

#If the ssim is less than this value the frames are different. Increase this for greater sensitivity. 
ssim_thresh_hold = 0.65

#Set to True to display the modified frames in a window 
display_frame = False

#Have a cool down timer between goals detected to minimize the chances of false positives.
coolval = 100
#~~~~~~~~~~~~~~~~~~CONFIG~~~~~~~~~~~~~~~~~~


def main():
    frame2 = np.array(ImageGrab.grab(bbox=(x, y, x2, y2)))
    cool = 0
    while(True):

        img = ImageGrab.grab(bbox=(x, y, x2, y2))
        frame = np.array(img)

        grayA = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        #Convert our image to black and white based on pixel intensity. This works because the score is displayed as a white font on orange/blue background, eliminating noise in our frame comparison.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        thresh_frame1 = cv2.threshold(grayA, 170, 255, cv2.THRESH_BINARY)[1] 
        thresh_frame1 = cv2.dilate(thresh_frame1, None, iterations = 2) 

        thresh_frame2 = cv2.threshold(grayB, 170, 255, cv2.THRESH_BINARY)[1] 
        thresh_frame2 = cv2.dilate(thresh_frame2, None, iterations = 2) 
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
        if display_frame:
            cv2.imshow('RocketLeague', thresh_frame1) #Display our modified frame

        (score, diff) = compare_ssim(thresh_frame1, thresh_frame2, full=True) #Compare the old and new frame for a SSIM score.
        diff = (diff * 255).astype("uint8")

        if score < ssim_thresh_hold:
            if cool == coolval:
                print("Goal!") #Do cool stuff here
                cool = 0 #Reset our counter after a goal is detecte
        
        if cool < coolval: #This block prevents the timer from contstatly counting upward to infinity if a goal is never detected
            cool += 1

        frame2 = frame

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()
