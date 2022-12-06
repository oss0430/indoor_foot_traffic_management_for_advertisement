import time

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

class Bilboard():

    def __init__(
        self,
        camera : Camera,
        screen : Screen,
        aws_cloud : AWSCloud,
        movement_sensor : MovementSensor
    ):
        self.camera = camera
        self.screen = screen
        self.aws_cloud = aws_cloud
        self.movement_sensor = movement_sensor

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