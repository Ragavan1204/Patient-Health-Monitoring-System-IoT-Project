# Patient-Health-Monitoring-System-IoT-Project
Here, we use the existing patient care monitors in the hospital to access the patient data. We connect our iot device with monitor using access port. Doctors can access the data through mobile app. Data can be accesed by hospital management through web dashboard. Doctors can set diffent throushhold for critcal parameters idividually for every patient. So they get alert when patient is in the critical condtion. Here we use Aws cloud to analize the data. It gives secure connection for data transfer. We use aws iot core to connect the the iot device. Aws lamda services to predict the complication. And,we used SNS services to give the alert to the doctors through sms.

This repository contains the details of collecting the data from the patient care monitor through IoT Device and send it to the cloud.we used mqqt protocol with X.509 certification to securely connect the iot device with cloud.Data logging software called VSCapture is running on our device. It collect the data such as Heart rate, Blood pressure, oxygen Saturation and Pulse of the patient and save it to the csv file.Then the aws client running on our device read csv file and publish the data for the corresponding topic.



