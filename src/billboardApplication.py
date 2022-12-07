import RPi.GPIO as GPIO
import picamera
import time
import datetime
import shutil
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
        self.stop_screen_event = threading.Event()
        self.new_image_event = threading.Event()


    def _show_image_from_path_on_screen(
        self,
        path
    ) -> None:

        while True:
            print("image_loop")
            image = cv2.imread(path)
            cv2.imshow("Billboard", image)
            key = cv2.waitKey(0)

            if self.new_image_event.is_set():
                cv2.destroyAllWindows()
                break

            if self.stop_screen_event.is_set():
                cv2.destroyAllWindows()
                break

        return

    def update_screen_with_new_image(self) -> None :
        self.new_image_event.set()


    def stop_screen_for_good(self) -> None:
        self.stop_screen_event.set()


    def run_screen(
        self,
        image_path : str     
    )-> None:

        self.stop_screen_event.clear()
        self.new_image_event.clear()

        while True:
            thread = threading.Thread(target = self._show_image_from_path_on_screen, args = (image_path,))
            thread.start()
            thread.join()
            self.new_image_event.clear()

            if self.stop_screen_event.is_set():
                self.stop_screen_event.clear()
                break

        return



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

    def publish_image_and_its_face_count(
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
        

    def subscribe_and_save_image(
        self,
        image_save_path : str,
    ) -> None:

        def callbackonAWSMessage(client, userdata, message):
            print('message recieved')
            self._read_image_from_json_message(message.payload, image_save_path)
    
        self.client.subscribe(self.subscribe_topic, 1, callback = callbackonAWSMessage)


    def testPublish(self):
        self.publish_image_and_its_face_count("test_img.png", 5)

    def testSubscribe(self):
        self.subscribe_and_save_image("subscribed_imaged_result.png")


class Billboard():

    def __init__(
        self,
        camera_controller : CameraController,
        screen_controller : ScreenController,
        aws_iot_controller : AWSIoTController, 
        ultrasound_sensor : UltraSoundSensor,
        billboard_image_path : str,
        camera_capture_dir_path : str,
        cascade_file_path : str,
    ) -> None:
        self.camera_controller = camera_controller
        self.screen_controller = screen_controller
        self.aws_iot_controller = aws_iot_controller
        self.ultrasound_sensor = ultrasound_sensor
        self.billboard_image_path = billboard_image_path
        self.camera_capture_dir_path = camera_capture_dir_path
        self.cascade_file_path = cascade_file_path
        
        self.new_billboard_image_arrive_event = threading.Event()
        self.close_billboard_for_good_event = threading.Event()


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


    def _keep_checking_face_and_publish(
        self
    ) -> bool:

        while True:
            
            if self.new_billboard_image_arrive_event.is_set():
                ## Untill New image is properly shown in screen
                ## Dont Send
                break

            if self.close_billboard_for_good_event.is_set():
                ## Clase Billboard for good Event
                ## Dont Send
                break


            if self.ultrasound_sensor.are_people_in_front_standing():
                self.camera_controller.take_picture_and_save_to_dir(self.camera_capture_dir_path)
                face_count = self._get_face_count_in_captured_image_recognition(do_save_boxed_image = True)
                self.aws_iot_controller.publish_image_and_its_face_count(image_path = self.camera_capture_dir_path + "/captured_boxed.png", face_count= face_count)
                print("yes_poeple")
                    
            else :
                print("no_people")
                time.sleep(1)

        return

    def _subscribe_to_aws_for_new_billboard_image(
        self
    ) -> str:
            
        while True:
            if self.close_billboard_for_good_event.is_set():
                break

            ## Keep Listening to Subscribtion
            self.aws_iot_controller.subscribe_and_save_image(self.billboard_image_path)
            
            ## If above line is done listening stops, subscribtion made
            ## Start updating image, untill update complete stop publishing
            self.new_billboard_image_arrive_event.set()
            self.screen_controller.update_screen_with_new_image()
            update_inprogress_condition = self.screen_controller.new_image_event

            while not update_inprogress_condition.is_set():
                time.sleep(0.01)

            ## Update Complete
            self.new_billboard_image_arrive_event.clear()

        return
        
    def stop_billboard(self)->None:
        self.close_billboard_for_good_event.set()
        
                        

    def run_billboard(
        self
    ):
        ## Shows Billboard image through screen
        ## update billboard image when subscription
        ## upload face recognition result when people is infront of billboard
        self.close_billboard_for_good_event.clear()

        while True:
            if self.close_billboard_for_good_event.is_set():
                self.screen_controller.stop_screen_for_good.set()
                self.aws_iot_controller.client.disconnect()
                break
            
            # Run Screen 
            self.screen_controller.run_screen(self.billboard_image_path)
            ## Thread a people checker
            
            keep_checking_face_thread = threading.Thread(target = self._keep_checking_face_and_publish)
            keep_updating_billboard_thread = threading.Thread(target = self._subscribe_to_aws_for_new_billboard_image)

            keep_checking_face_thread.join()
            keep_updating_billboard_thread.join()
            
        return

class ApplicationTester():
    def __init__(
        self
    ) :
        None

    def test_billboard(
        self
    ):

        camera_capture_dir_path = "./captured_image"
        cascade_file_path = "haarcascade_frontalface_default.xml"
        aws_config_json_path = "aws_config.json"
        billboard_image_path = "billboard_image.png"


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
        my_billboard = Billboard(
            camera_controller = my_camera_controller,
            screen_controller = my_screen_controller,
            aws_cloud = my_aws_iot_controller,
            ultrasound_sensor = my_ultra_sound_sensor,
            billboard_image_path = billboard_image_path,
            camera_capture_dir_path = camera_capture_dir_path,
            cascade_file_path = cascade_file_path,
        )

        my_billboard.run_billboard()


    def testScreenController(
        self,
        original_image_path : str,
        new_image_path : str
    ):
        copy_path = "test_copy_image.png"

        shutil.copyfile(original_image_path, copy_path)

        my_screen_controller = ScreenController()

        threading.Thread(target = my_screen_controller.run_screen, args = (copy_path,))
        time.sleep(3)
        shutil.copyfile(new_image_path, copy_path)
        my_screen_controller.update_screen_with_new_image()
        time.sleep(3)

        
        my_screen_controller.stop_screen_for_good()
        
        if os.path.isfile(copy_path):
            os.remove(copy_path)

        return