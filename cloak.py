import cv2
import numpy as np

input_color = input("Enter the color of the cloak (red, green, blue): ")

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

saved_frame = None

def apply_green_screen(bg_frame):
    ret, frame = cam.read()

    if not ret:
        print("failed to grab frame")
        return ret, frame
    else:

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #green bounds
        if input_color == "green":
        
            lower_green = np.array([40, 40, 40])
            upper_green = np.array([80, 255, 255])

            mask = cv2.inRange(hsv, lower_green, upper_green)
        #red bounds
        elif input_color == 'red':
            lower_red1 = np.array([0, 120, 70])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 120, 70])
            upper_red2 = np.array([180, 255, 255])
            
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

            mask = cv2.bitwise_or(mask1, mask2)

        elif input_color == 'blue':
            #blue bounds
            lower_blue = np.array([100, 150, 0])
            upper_blue = np.array([140, 255, 255])


            mask = cv2.inRange(hsv, lower_blue, upper_blue)

        mask_inv = cv2.bitwise_not(mask)

        fg = cv2.bitwise_and(frame, frame, mask=mask_inv)

        bg = cv2.bitwise_and(bg_frame, bg_frame, mask=mask)

        new_frame = cv2.add(bg, fg)
        
        return ret, new_frame

while True:
    if saved_frame is None:
        ret, frame = cam.read()
    else:
        ret, frame = apply_green_screen(saved_frame)
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        saved_frame = frame
        cv2.imwrite("saved_frame.png", saved_frame)
        

cam.release()

cv2.destroyAllWindows()