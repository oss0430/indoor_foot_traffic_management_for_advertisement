import RPi.GPIO as GPIO
import picamera
import time
import os
import cv2
import sys


class UltraSoundSensor():
    def __init__(
        self,
        trigger_pin_BCM : int = 2,
        echo_pin_BCM : int = 3
    ) -> None:
        GPIO.setmode(GPIO.BCM)
        self.trigger_pin_BCM = trigger_pin_BCM
        self.echo_pin_BCM = echo_pin_BCM
        self.is_in_front_upperbound_cm = 50.0

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

    def are_people_in_front_standing(self) -> bool:
        
        three_checks = [False, False, False]

        if self._echo_location_by_cm() < self.is_in_front_upperbound_cm :
            three_checks[0] = True
        if self._echo_location_by_cm() < self.is_in_front_upperbound_cm :
            three_checks[1] = True
        if self._echo_location_by_cm() < self.is_in_front_upperbound_cm :
            three_checks[2] = True

        if False in three_checks:
            return False
        
        else :
            return True


class CameraController():

    ## A camera class for smart billbaords camera application

    def __init__(
        self,
        correct_rotation : str ="90",
        resolution : tuple = (640, 400)

    ) -> None:
        self.correct_rotation = correct_rotation,
        self.resolution = resolution

    def take_picture_and_save_to_dir(
        self,
        dir_path : str
    ):
        camera = picamera.PiCamera()
        camera.rotation = 90
        camera.resolution = (640, 400)
        camera.start_preview()
        camera.capture(dir_path + "/captured_image.png")
        camera.close()

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
        camera_controller : CameraController,
        screen ,#: Screen,
        aws_cloud , #: AWSCloud,
        ultrasound_sensor : UltraSoundSensor,
        billboard_image_path : str,
        camera_capture_dir_path : str,
        cascade_file_path : str,
    ) -> None:
        self.camera_controller = camera_controller
        self.screen = screen
        self.aws_cloud = aws_cloud
        self.ultrasound_sensor = ultrasound_sensor
        self.billboard_image_path = billboard_image_path
        self.camera_capture_dir_path = camera_capture_dir_path
        self.cascade_file_path = cascade_file_path

    def _listen_for_image_update(self):
        return self.movement_sensor()

    def _create_json_classification_payload(self):
        ## Create Test Result
        return

    def _create_json_capture_payload(self):
        return

    def _get_face_count_in_captured_image_recognition(
        self,
        do_save_boxed_image : bool = True
    ) -> int:

        face_cascade = cv2.CascadeClassifier(self.cascade_file_path)
        image = cv2.imread(self.camera_capture_dir_path + "/captured_image.png")
        gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors= 5,
            minSize=(30,30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )

        for (x,y,w,h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if do_save_boxed_image :
            cv2.imwrite(self.camera_capture_dir_path + "/captured_boxed.png" ,image)

        return len(faces)
    
    def run_billboard(
        self
    ):
        ## Shows Test Billboard image through screen
        ## upload face recognition result to aws
        ## Along with Billboard image id (for AB TESTING)
        while True:
            
            if self.ultrasound_sensor.are_people_in_front_standing():
                print("yes_poeple")
                break
            else :
                print("no_people")
                time.sleep(1)

        self.camera_controller.take_picture_and_save_to_dir(self.camera_capture_dir_path)
        return self._get_face_count_in_captured_image_recognition(True)
