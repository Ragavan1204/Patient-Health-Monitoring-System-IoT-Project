import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import time as t
import json
import logging

# initialize parameters
prevous_parameters={"Date": 1/1/2000, "Time": "00:00:00" , "pulse":0,"heart_rate":0,"ox_saturation":0}
current_parameters={"Date": 1/1/2000, "Time": "00:00:00" , "pulse":0,"heart_rate":0,"ox_saturation":0}


# configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


# Divice confiquration
ENDPOINT = "a2xz6bh1uzu45n-ats.iot.us-west-2.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "certificates/device.pem.crt"
PATH_TO_PRIVATE_KEY = "certificates/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/Amazon-root-CA-1.pem"

# mqtt confiquration
myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)


# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

TOPIC= CLIENT_ID + "/parameters"


def get_data():
    # read csv file
    with open('sample patient data.csv','r') as file: 
	    data = file.readlines() 
    lastRow = data[-1].split(',')  # get the last row data
     

    # according to the csv file format, indexes of health parameters
    # date - 0
    # time - 1
    # heart_rate -2
    # ox_satur - 6
    # Pulse - 9

    #update current_parameters
    current_parameters["Date"]=lastRow[0]
    current_parameters["Time"]=lastRow[1]
    current_parameters["pulse"]=lastRow[9]
    current_parameters["heart_rate"]=lastRow[2]
    current_parameters["ox_saturation"]=lastRow[6]




# check the last row data is the new data
def is_data_new():
    Current_time= current_parameters["Time"].split(':')
    previous_time= prevous_parameters["Time"].split(':')

    Current_time = list(map(int, Current_time))
    previous_time = list(map(int, previous_time))
    print(Current_time,previous_time)
    
    if (Current_time == previous_time):
        return False
    else:
        return True
    

# Publish the data  at every 5 minute
while(1):

    get_data() # update the current parameters by reading the last row in csv file
    
    if (is_data_new()):
        myAWSIoTMQTTClient.connect()
        print('Begin Publish')
        myAWSIoTMQTTClient.publish(TOPIC, json.dumps(current_parameters), 1) 
        print("Published: '" + json.dumps(current_parameters) + "' to the topic: "+ TOPIC)
        print('Publish End')
        myAWSIoTMQTTClient.disconnect()

    prevous_parameters=current_parameters
    t.sleep(20)

    
