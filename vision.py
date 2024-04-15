import cv2
import numpy as np


def detect_orange_ball(image):
    # convert image to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # define range of orange color in HSV
    lower_orange = np.array([10, 100, 100])
    upper_orange = np.array([20, 255, 255])
    # threshold the HSV image to get only orange colors
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)


    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        return (int(x), int(y), int(radius))
    return None

def draw_circle(image, ball):
    cv2.circle(image, (ball[0], ball[1]), ball[2], (0, 255, 0), 2)
    
def draw_center(image):
    height, width = image.shape[:2]
    cv2.line(image, (0, height//2), (width, height//2), (0, 0, 255), 2)
    cv2.line(image, (width//2, 0), (width//2, height), (0, 0, 255), 2)


def main():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (1920, 1080))
        print(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(frame.shape)
        if not ret:
            break
        ball = detect_orange_ball(frame)
        if ball:
            draw_circle(frame, ball)
            print(f"Ball position: {ball[0]}, {ball[1]}")
        draw_center(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
