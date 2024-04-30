from AdafruitMotor import AdafruitMotor
from AdafruitRover import AdafruitRover
import serial
import time
import cv2
from FaceDetector import FaceDetector

# Initialize the Rover with motor instances
motor_front_left = AdafruitMotor(1)  # Motor 1 is the front left motor
motor_front_right = AdafruitMotor(2)  # Motor 2 is the front right motor
motor_back_left = AdafruitMotor(3)  # Motor 3 is the back left motor
motor_back_right = AdafruitMotor(4)  # Motor 4 is the back right motor
rover = AdafruitRover(motor_front_left, motor_front_right, motor_back_left, motor_back_right)

# Serial communication set up
serial_port = "/dev/ttyUSB0"
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Initialize the face detector with the Haar Cascade XML file
face_detector = FaceDetector('haarcascade_frontalface_default.xml')

# Initialize video capture with the default webcam
cap = cv2.VideoCapture(0)

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8").rstrip()
            try:
                distance = float(line)
                print(f"Distance: {distance} cm")

                if distance < 10:
                    # Stop rover if obstruction is within 10 cm
                    rover.stop()
                    print("Obstruction detected. Stopping.")
                else:
                    # Ask user for input
                    direction = input("Enter direction (f, b, l, r): ").lower()
                    # Move rover based on user input
                    if direction == "f":
                        rover.forward(.5)
                        time.sleep(1)
                        rover.stop()
                        continue
                    elif direction == "b":
                        rover.backward(.5)
                        time.sleep(1)
                        rover.stop()
                        continue
                    elif direction == "l":
                        rover.left(.5)
                        time.sleep(1)
                        rover.stop()
                        continue
                    elif direction == "r":
                        rover.right(.5)
                        time.sleep(1)
                        rover.stop()
                        continue
                    else:
                        print("Invalid direction. Please enter forward, backward, left, or right.")
            except ValueError:
                # Handle cases where the distance reading is not a valid float
                print(f"Error. Received bad data: {line}")

        # Capture a frame from the camera
        _, frame = cap.read()

        # Detect faces
        faces = face_detector.detect_faces(frame)

        # Draw rectangles around faces
        frame_with_faces = face_detector.draw_faces(frame, faces)

        # Display the frame with detected faces
        cv2.imshow('Live Feed', frame_with_faces)

        # Wait for a key press and check if the user pressed 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Pause for a short while to control the frame rate
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped by user.")
finally:
    # Ensure motors are stopped and serial port is closed when program ends
    rover.stop()
    ser.close()
