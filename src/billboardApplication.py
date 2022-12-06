import RPi.GPIO as GPIO
import time

class UltraSoundSensor():
    def __init__(
        self,
        trigger_pin_BCM : int = 2,
        echo_pin_BCM : int = 3
    ) -> None:
        GPIO.setmode(GPIO.BCM)
        self.trigger_pin_BCM = trigger_pin_BCM
        self.echo_pin_BCM = echo_pin_BCM
        
        GPIO.setup(trigger_pin_BCM, GPIO.OUT)
        GPIO.setup(echo_pin_BCM, GPIO.IN)


    def _echo_location_by_cm(self) -> float:
        GPIO.output(self.trigger_pin_BCM, True)
        ## Delay for 10uS pulse
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin_BCM, False)

        while GPIO.input(self.echo_pin_BCM) == 0:
            pulse_start = time.time()

        while GPIO.input(self.echo_pin_BCM) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 34300 / 2
        distance = round(distance, 4)

        time.sleep(0.4)

        return distance



class MovementSensor():

    def __init__(self) -> None:
        return

    def detect_movement(self):
        ## In different Thread keep detecting untill it spots movement

        is_movement = True
        
        return is_movement


class Camera():

    ## A camera class for smart billbaords camera application

    def __init__(self) -> None:
        return

    def _takePicture(self):
        return

    def _savePicture(self):
        return

    def runByTimer(self) -> None:
        return

class Screen():
    def __init__(self) -> None:
        return

    def showOnScreen(self) -> None:
        return

class AWSCloud():
    def __init__(self
    ) -> None:

        return

class Billboard():

    def __init__(
        self,
        camera : Camera,
        screen : Screen,
        aws_cloud : AWSCloud,
        movement_sensor : MovementSensor,
        ultrasound_sensor : UltraSoundSensor,
    ):
        self.camera = camera
        self.screen = screen
        self.aws_cloud = aws_cloud
        self.movement_sensor = movement_sensor
        self.ultrasound_sensor = ultrasound_sensor

    def _is_movement(self):
        return self.movement_sensor()


    def run_test(
        self
    ):
        ## Shows Test Billboard image through screen
        ## upload face recognition result to aws
        ## Along with Billboard image id (for AB TESTING)

        self.movement_sensor.detect_movement()

        None