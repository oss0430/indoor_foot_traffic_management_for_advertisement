import RPi.GPIO as GPIO
from billboardApplication import *

GPIO.cleanup()

my_ultra_sound_sensor = UltraSoundSensor()
my_camera_controller = CameraController(
    correct_rotation = "90",
    resolution = (640, 400)
)

camera_capture_dir_path = "./captured_image"
cascade_file_path = "haarcascade_frontalface_default.xml"


my_billboard = Billboard(
    camera_controller = my_camera_controller,
    screen = None,#: Screen,
    aws_cloud = None, #: AWSCloud,
    ultrasound_sensor = my_ultra_sound_sensor,
    billboard_image_path = "",
    camera_capture_dir_path = camera_capture_dir_path,
    cascade_file_path = cascade_file_path,
)
for i in range(0,5):
    my_billboard.run_billboard()

GPIO.cleanup()
    



