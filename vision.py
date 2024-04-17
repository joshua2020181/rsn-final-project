import cv2
import numpy as np
import serial
import time

ARDUINO_PORT = '/dev/ttyUSB0'
ARDUINO_BAUDRATE = 115200

MAX_SEND_RATE = 0.2  # seconds

serial_port = serial.Serial(ARDUINO_PORT, ARDUINO_BAUDRATE)
print("Serial port opened")

last_sent = time.time()

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

def move_motors(ball, center):
    pan_val = 0
    tilt_val = 0
    if ball[0] < center[0]:
        # print("Move left")
        pan_val = -60
    elif ball[0] > center[0]:
        # print("Move right")
        pan_val = 60
    if ball[1] < center[1]:
        # print("Move up")
        tilt_val = 50
    elif ball[1] > center[1]:
        # print("Move down")
        tilt_val = -50
    print(f"Pan: {pan_val}, Tilt: {tilt_val}")
    global last_sent
    if time.time() - last_sent > MAX_SEND_RATE:
        last_sent = time.time()
        serial_port.write(f"{pan_val};{tilt_val}\n".encode())


def main():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        center_x, center_y = frame.shape[1]//2, frame.shape[0]//2
        if not ret:
            break
        ball = detect_orange_ball(frame)
        if ball:
            draw_circle(frame, ball)
            # print(f"Ball position: {ball[0]}, {ball[1]}")
            move_motors(ball, (center_x, center_y))
        else:
            move_motors((center_x, center_y), (center_x, center_y))
        draw_center(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
