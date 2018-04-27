from kafka import KafkaConsumer
import sys
sys.path.append("..")

from util.config import Config
from trigger.trigger import Trigger
from database.database import Database

class Listener():
    def __init__(self):
        self.stopFlag = False
        self.database = Database()
        self.configObj = Config()
        self.triggerObj = Trigger()
        self.listenerObj = KafkaConsumer(bootstrap_servers=self.configObj.KAFKA_QUEUE_HOSTNAME_PORT,
                                 auto_offset_reset='latest',
                                 consumer_timeout_ms=1000)

    # Emergency Stop the listener
    def stop(self):
        self.stopFlag = True


    # Run the service to listen to the kafka queue on particular topic
    def startListening(self, ):

        while not self.stopFlag:
            topics = listener.database.getAllKafkaTopics()
            topics.append('Topic1')
            self.listenerObj.subscribe(topics)
            print 'Topics', self.listenerObj.topics()
            print 'Subscriptions', self.listenerObj.subscription()
            for message in self.listenerObj:
                print 'Message', message
                # As soon as the request is listened from the Kafka Queue, Invoke the trigger
                self.triggerObj.handleRequest(message)

                if self.stopFlag == True:
                    break

        self.listenerObj.close()

if __name__ == "__main__":
    listener = Listener()
    listener.startListening()
