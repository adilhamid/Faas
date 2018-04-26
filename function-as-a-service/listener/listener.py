from kafka import KafkaConsumer
import sys
sys.path.append("..")

from util.config import Config
from trigger.trigger import Trigger
from database.database import Database
import polling

class Listener():
    def __init__(self):
        self.stopFlag = False
        self.database = Database()
        self.configObj = Config()
        self.triggerObj = Trigger()
        self.listenerObj = KafkaConsumer(bootstrap_servers=self.configObj.KAFKA_QUEUE_HOSTNAME_PORT,
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000)

    # Emergency Stop the listener
    def stop(self):
        self.stopFlag = True


    # Run the service to listen to the kafka queue on particular topic
    def startListening(self, topics):
        self.listenerObj.subscribe(topics)

        while not self.stopFlag:
            for message in self.listenerObj:
                print(message)
                # As soon as the request is listened from the Kafka Queue, Invoke the trigger
                self.triggerObj.handleRequest(message)

                if self.stopFlag == True:
                    break

        self.listenerObj.close()

def listenerListe(listener):
    listener.stopFlag = True
    topics = listener.database.getAllKafkaTopics()
    print 'Topics Listening to ', topics
    listener.startListening(topics)
    listener.stopFlag = False

if __name__ == "__main__":
    listener = Listener()
    polling.poll(lambda :listenerListe(listener), step=60, poll_forever = True)