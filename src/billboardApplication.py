import RPi.GPIO as GPIO
import picamera
import time
import datetime
import os
import cv2
import json
import base64
import numpy as np
import sys
import threading
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from cloud_config import AWSMQTTConfig

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


class ScreenController():
    def __init__(
        self    
    ) -> None:
        return

    def _show_image_from_path_on_screen(
        self,
        path
    ) -> None:

        image = cv2.imread(path)
        cv2.imshow("Faces found", image)

        return

    def terminate_existing_image_thread(self):
        None

    def create_thread_that_show_image(self):
        None 

"""

class ImageShowingThread(Thread):
    def on_thread_finished(
        self,
        thread,
        data
    ):
        pass

    def __init__(
        self,
        secreen_controller : ScreenController
    ):
        self.parent = parent


    def run(self):
        self.parent and self.parent.
"""

class AWSIoTController():
    def __init__(
        self,
        client_name : str,
        cloud_config : AWSMQTTConfig,
        publish_topic : str,
        subscribe_topic : str
    ) -> None:

        self.client_name = client_name
        self.cloud_config = cloud_config
        client = AWSIoTPyMQTT.AWSIoTMQTTClient(client_name)
        client.configureEndpoint(cloud_config.host_name, 8883) 
        client.configureCredentials(cloud_config.root_ca_path, cloud_config.private_key_path, cloud_config.cert_file_path) 
        client.configureConnectDisconnectTimeout(cloud_config.disconnection_timeout) 
        client.configureMQTTOperationTimeout(cloud_config.mqtt_operation_timeout)
        
        def awsConnectCallback(mid, data):
            print("AWS connected")

        #client.connectAsync(ackCallback=awsConnectCallback)     
        client.connect()
        
        self.client = client
        self.publish_topic = publish_topic
        self.subscribe_topic = subscribe_topic


    def _read_image_file_as_message_for_publishing(
        self,
        file_path : str
    ) -> str:
        img = cv2.imread(file_path, cv2.IMREAD_COLOR)
        _, img_jpg = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        b64 = base64.b64encode(img_jpg)
        messageJson = json.dumps(
            {
                'device_name' : self.client_name,
                'image':b64.decode("utf-8"),
                'datetime' : datetime.datetime.now().strftime("%Y%M%D_%H:%M:%S")
            }
        )
            
    
        return messageJson

    def _read_image_from_json_message(
        self,
        message_json :str,
        image_save_path : str
    ) -> np.ndarray:
         
        b64 = json.loads(message_json)

        img_jpg = base64.b64decode(b64['image'])
        img_na = cv2.imdecode(np.frombuffer(img_jpg,dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imwrite(image_save_path, img_na) 

        return img_na

    def _publish_image_and_its_face_count(
        self,
        image_path : str,
        face_count : int
    ) -> None:

        image_json = self._read_image_file_as_message_for_publishing(image_path)
        def awsPublishcallback(mid):
            print("AWS Publish") 
        
        faceCount_json = json.dumps(
            {
                'device_name' : self.client_name,
                'facecount':face_count,
                'datetime' : datetime.datetime.now().strftime("%Y%M%D_%H:%M:%S")
            }
        )
        #print("json_messages : ",faceCount_json, image_json)
            
        self.client.publishAsync(self.publish_topic+"/"+self.clinet_name +"/image", image_json, 1, ackCallback=awsPublishcallback)
        self.client.publishAsync(self.publish_topic+"/"+self.clinet_name +"/face_count", faceCount_json, 1, ackCallback=awsPublishcallback)
        

    def _subscribe_and_save_image(
        self,
        image_save_path : str,
    ) -> None:
        def awsSubscribeCallback(mid, data):
            print("AWS Subscribed")
    
        def callbackonAWSMessage(client, userdata, message):
            print('message recieved')
            self._read_image_from_json_message(message.payload, image_save_path)
    
        self.client.subscribeAsync(self.subscribe_topic, 1, ackCallback = awsSubscribeCallback, messageCallback = callbackonAWSMessage)


    def testPublish(self):
        self._publish_image_and_its_face_count("test_img.png", 5)

    def testSubscribe(self):
        self._subscribe_and_save_image("subscribed_imaged_result.png")


class Billboard():

    def __init__(
        self,
        camera_controller : CameraController,
        screen ,#: Screen,
        aws_cloud : AWSIoTController, 
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
        
        
        ## Thread a people checker
        def keep_checking_face(
            ultrasound_sensor : UltraSoundSensor,
            aws_cloud : AWSIoTController
        ) -> bool:

            while True:
                if ultrasound_sensor.are_people_in_front_standing():
                    ## Upload Image to cloud
                    aws_cloud._publish_image_and_its_face_count
                    print("yes_poeple")
                    
                else :
                    print("no_people")
                time.sleep(1)
            

        
        def subscribe_to_aws_for_new_billboard_image(
            aws_iot_controller : AWSIoTController,
            image_save_path : str,
            screen_controller : ScreenController
        ) -> str:
            screen_controller.terminate_existing_image_thread()
            aws_iot_controller._subscribe_and_save_image(image_save_path)
            screen_controller.create_thread_that_show_image()
            
        
            
            

        self.camera_controller.take_picture_and_save_to_dir(self.camera_capture_dir_path)
        return self._get_face_count_in_captured_image_recognition(True)
