#import RPi.GPIO as GPIO
from cloud_config import AWSMQTTConfig
from billboardApplication import *

"""
camera_capture_dir_path = "./captured_image"
cascade_file_path = "haarcascade_frontalface_default.xml"
aws_config_json_path = "aws_config.json"
test_img = "test_img.png"

GPIO.cleanup()

my_ultra_sound_sensor = UltraSoundSensor()
my_camera_controller = CameraController(
    correct_rotation = "90",
    resolution = (640, 400)
)
my_cloud_config = AWSMQTTConfig()
my_cloud_config.read_config_json(aws_config_json_path)

my_aws_iot_controller = AWSIoTController(
    "0",
    my_cloud_config,
    "billboard/pub",
    "billboard/sub"
)

my_screen_controller = ScreenController()
my_screen_controller.run_screen(test_img)

while True:
    command = input("input command n, x : ")
    
#my_aws_iot_controller.testPublish()
#print("test_complete")

my_billboard = Billboard(
    camera_controller = my_camera_controller,
    screen = None,#: Screen,
    aws_cloud = my_aws_iot_controller,
    ultrasound_sensor = my_ultra_sound_sensor,
    billboard_image_path = "",
    camera_capture_dir_path = camera_capture_dir_path,
    cascade_file_path = cascade_file_path,
)

GPIO.cleanup()
time.sleep(1000000)    
"""

tester = ApplicationTester()

tester.testScreenController(original_image_path= "test_img.png", new_image_path="../img/System_cloud.PNG")



