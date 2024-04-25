from AdafruitMotor import AdafruitMotor

class AdafruitRover:
    def __init__(self, motor_front_left, motor_front_right, motor_back_left, motor_back_right):
        self.motor_front_left = motor_front_left
        self.motor_front_right = motor_front_right
        self.motor_back_left = motor_back_left
        self.motor_back_right = motor_back_right
        
    def forward(self, speed=1.0):
        # Move forward at specified speed
        self.motor_front_left.move_forward(speed)
        self.motor_front_right.move_forward(speed)
        self.motor_back_left.move_forward(speed)
        self.motor_back_right.move_forward(speed)
        
    def backward(self, speed=1.0):
        # Move backward at specified speed
        self.motor_front_left.move_backward(speed)
        self.motor_front_right.move_backward(speed)
        self.motor_back_left.move_backward(speed)
        self.motor_back_right.move_backward(speed)
        
    def left(self, speed=1.0):
        # Turn the rover left by reducing the speed of the left motors
        self.motor_front_left.move_forward(speed / 2)
        self.motor_front_right.move_forward(speed)
        self.motor_back_left.move_forward(speed / 2)
        self.motor_back_right.move_forward(speed)
        
    def right(self, speed=1.0):
        # Turn the rover right by reducing the speed of the right motors
        self.motor_front_left.move_forward(speed)
        self.motor_front_right.move_forward(speed / 2)
        self.motor_back_left.move_forward(speed)
        self.motor_back_right.move_forward(speed / 2)
        
        
    def stop(self):
        # Stop all motors
        self.motor_front_left.move_stop()
        self.motor_front_right.move_stop()
        self.motor_back_left.move_stop()
        self.motor_back_right.move_stop()
        
    def validate_speed(self, speed):
        # Ensure the speed does not exceed the maximum allowable value
        if speed < 0 or speed > 1:
            raise ValueError("Speed must be between 0 and 1.")
        