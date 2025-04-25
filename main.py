import cv2
import time

# Load Haar cascade for car detection
car_cascade = cv2.CascadeClassifier('car.xml')  # Make sure this is in the same folder!

# Use Pi camera (or 0 for webcam)
cap = cv2.VideoCapture(0)
time.sleep(2)  # Warm-up

def draw_traffic_light(frame, state, time_left):
    # Traffic light background
    cv2.rectangle(frame, (580, 50), (640, 170), (50, 50, 50), -1)
    
    # Light positions
    positions = [(610, 70), (610, 110), (610, 150)]  # Red, Yellow, Green

    # Colors based on state
    colors = [(0, 0, 255), (0, 255, 255), (0, 255, 0)]
    active = {'red': 0, 'yellow': 1, 'green': 2}[state]

    for i, (x, y) in enumerate(positions):
        color = colors[i] if i == active else (30, 30, 30)
        cv2.circle(frame, (x, y), 12, color, -1)

    # Display state and timer
    cv2.putText(frame, f"{state.capitalize()} {time_left}s", (430, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, colors[active], 2)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 9)
    num_cars = len(cars)

    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.putText(frame, f"Cars Detected: {num_cars}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.imshow('Traffic Camera', frame)

    if num_cars > 0:
        green_time = num_cars * 5
        red_time = num_cars * 3

        for i in range(green_time):
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (640, 480))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cars = car_cascade.detectMultiScale(gray, 1.1, 9)
            for (x, y, w, h) in cars:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            draw_traffic_light(frame, 'green', green_time - i)
            cv2.imshow('Traffic Camera', frame)
            if cv2.waitKey(1000) == 27:
                break

        for i in range(red_time):
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (640, 480))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cars = car_cascade.detectMultiScale(gray, 1.1, 9)
            for (x, y, w, h) in cars:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            draw_traffic_light(frame, 'red', red_time - i)
            cv2.imshow('Traffic Camera', frame)
            if cv2.waitKey(1000) == 27:
                break
    else:
        draw_traffic_light(frame, 'yellow', 3)
        cv2.imshow('Traffic Camera', frame)
        if cv2.waitKey(1000) == 27:
            break

cap.release()
cv2.destroyAllWindows()
