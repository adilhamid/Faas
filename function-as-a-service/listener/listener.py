from kafka import KafkaConsumer
import sys
sys.path.append("..")

from config import CONFIG
from trigger.trigger import Trigger

class Listener():
    def __init__(self):
        self.stopFlag = False
        self.triggerObj = Trigger()
        self.listenerObj = KafkaConsumer(bootstrap_servers=CONFIG.KAFKA_QUEUE_HOSTNAME_PORT,
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000)

    # Emergency Stop the listener
    def stop(self):
        self.stopFlag = True


    # Run the service to listen to the kafka queue on particular topic
    def startListening(self, topicName):
        self.listenerObj.subscribe([topicName])

        while not self.stopFlag:
            for message in self.listenerObj:
                print(message)
                # As soon as the request is listened from the Kafka Queue, Invoke the trigger
                self.triggerObj.handleRequest(self,message.value)

                if self.stopFlag == True:
                    break

        self.listenerObj.close()

# Example Usage
if __name__ == "__main__":
    Listener().startListening('function1')
