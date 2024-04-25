from flask import Flask, render_template, Response, request
import eventlet
import eventlet.wsgi
from AdafruitMotor import AdafruitMotor
from AdafruitRover import AdafruitRover
from flask_socketio import SocketIO, emit
import serial
import time
from CameraStream import CameraStream

# Necessary for using 'green threads' with Flask, improving concurrent handling of connections
eventlet.monkey_patch()

app = Flask(__name__)
# Initialize SocketIO with the Flask app, enabling real-time bi-directional communication
socketio = SocketIO(app)

# Initialize the Rover with motor instances
motor_front_left = AdafruitMotor(1)  # Motor 1 is the front left motor
motor_front_right = AdafruitMotor(2)  # Motor 2 is the front right motor
motor_back_left = AdafruitMotor(3) # Motor 3 is the back left motor
motor_back_right = AdafruitMotor(4) # Motor 4 is the back right motor
rover = AdafruitRover(motor_front_left, motor_front_right, motor_back_left, motor_back_right)

# Serial communication set up
serial_port = "/dev/ttyUSB0"
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Initialize the camera stream for live video feed
camera = CameraStream()

@app.route('/')
def index():
    # Serve the main HTML page for the rover control interface
    return render_template('index.html')

@socketio.on('control')
def handle_control(message):
    # Handle movement commands received via WebSocket
    direction = message['direction']
    moving = message['moving']
    
    # Log the direction and status of the movement
    if moving:
        print(f'Start moving {direction}')
        # Execute movement commands through the rover object based on direction
        if direction == 'forward':
            rover.forward()
        elif direction == 'backward':
            rover.backward()
        elif direction == 'left':
            rover.left()
        elif direction == 'right':
            rover.right()
    else:
        print(f'Stop moving {direction}')
        rover.stop()
        

def read_serial_data():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            try:
                distance = float(line)
                if distance < 10:
                    rover.stop()
                    print("Obstruction detected. Stopping.")
                    # Emit an event to disable the forward button
                    socketio.emit('obstruction', {'direction': 'forward', 'status': 'blocked'})
                else:
                    # Emit an event to enable the forward button if previously blocked
                    socketio.emit('obstruction', {'direction': 'forward', 'status': 'clear'})
                print(f"Distance: {distance} cm")
            except ValueError:
                print(f"Error. Received bad data: {line}")
        time.sleep(0.1)


@app.route('/video_feed')
def video_feed():
    # Endpoint for streamin ghte video feed from the rover's camera
    # Utilizes multipart/x-mixed-replace for MJPEG streaming
    return Response(camera.frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Run the Flask application with SocketIO on port 8080
    socketio.start_background_task(read_serial_data)
    socketio.run(app, host='0.0.0.0', port=8080)