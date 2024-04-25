from adafruit_motorkit import MotorKit

class AdafruitMotor:
    def __init__(self, motor_id):
        # Initialize the motor controller hat
        self.kit = MotorKit()
        
        # Assign the correct motor based on the motor_id
        if motor_id == 1:
            self.motor = self.kit.motor1
        elif motor_id == 2:
            self.motor = self.kit.motor2
        elif motor_id == 3:
            self.motor = self.kit.motor3
        elif motor_id == 4:
            self.motor = self.kit.motor4
        else:
            # Raise an error if the motor ID is not within the expected range
            raise ValueError("Invalid motor ID. Choose a value between 1 and 4.")
        
    def move_forward(self, speed=1.0):
        # Set the motor throttle to a positive value to move forward
        self.motor.throttle = speed
        
    def move_backward(self, speed=1.0):
        # Set the motor throttle to a negative value to move backward
        self.motor.throttle = -speed
        
    def move_stop(self):
        # Set the motor throttle to zero to stop the motor
        self.motor.throttle = 0