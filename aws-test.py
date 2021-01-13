from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

# 初期化
myMQTTClient = AWSIoTMQTTClient("Raspberry_Pi")

# MQTTクライアントの設定
myMQTTClient.configureEndpoint("a1zgqp33rfoox1-ats.iot.ap-northeast-1.amazonaws.com", 443)
myMQTTClient.configureCredentials("/home/pi/Parsonar-Project/Personal-Project/cert/AmazonRootCA1.pem", "/home/pi/Parsonar-Project/Personal-Project/cert/af5b640a0a-private.pem.key", "/home/pi/Parsonar-Project/Personal-Project/cert/af5b640a0a-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)

# Connect to AWS IoT endpoint and publish a message
myMQTTClient.connect()
print ("Connected to AWS IoT")
myMQTTClient.publish("awsiot/test", json.dumps({"test": "test message!"}), 0)
myMQTTClient.disconnect()
