import cv2
import numpy as np

def nothing(x):
    pass

def tweakHSL(img, thresh=(150, 255)):
    hsl_img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    h, l, s = cv2.split(hsl_img)
    cv2.namedWindow('image')
    
    cv2.createTrackbar('lowH','image',0,179,nothing)
    cv2.createTrackbar('highH','image',179,179,nothing)
    
    cv2.createTrackbar('lowL','image',0,255,nothing)
    cv2.createTrackbar('highL','image',255,255,nothing)
    
    cv2.createTrackbar('lowS','image',0,255,nothing)
    cv2.createTrackbar('highS','image',255,255,nothing)
    while(True):
        frame = img
    
        # get current positions of the trackbars
        ilowH = cv2.getTrackbarPos('lowH', 'image')
        ihighH = cv2.getTrackbarPos('highH', 'image')
        ilowL = cv2.getTrackbarPos('lowL', 'image')
        ihighL = cv2.getTrackbarPos('highL', 'image')
        ilowS = cv2.getTrackbarPos('lowS', 'image')
        ihighS = cv2.getTrackbarPos('highS', 'image')
        
        # convert color to hsv because it is easy to track colors in this color model
        hsl = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
        lower_hsl = np.array([ilowH, ilowL, ilowS])
        higher_hsl = np.array([ihighH, ihighL, ihighS])
        # Apply the cv2.inrange method to create a mask
        mask = cv2.inRange(hsl, lower_hsl, higher_hsl)
        # Apply the mask on the image to extract the original color
        frame = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow('image', frame)
        # Press q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def main():
    img = cv2.imread('./code/rgb2_image.jpg') # TODO: Replace with the path to the image you want to test
    tweakHSL(img)
    
if __name__ == "__main__":
    main()