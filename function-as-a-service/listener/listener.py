from kafka import KafkaConsumer

import multiprocessing
import sys

sys.path.append("..")
from config import CONFIG
from trigger.trigger import Trigger

class Listener(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stopFlag = multiprocessing.Event()
        self.triggerObj = Trigger()
        # The KAFKA_QUEUE_HOSTNAME_PORT is coming from config
        self.listenerObj = KafkaConsumer(bootstrap_servers=CONFIG.KAFKA_QUEUE_HOSTNAME_PORT,
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000)

    # Emergency Stop the listener
    def stop(self):
        self.stopFlag.set()

    # Run the service to listen to the kafka queue on particular topic
    def run(self):
        self.listenerObj.subscribe(['function1'])

        while not self.stopFlag.is_set():
            for message in self.listenerObj:
                print(message)
                # producer.send('topic', {'key': 'val'})
                assert isinstance(message.value, dict)
                # As soon as the request is listened from the Kafka Queue, Invoke the trigger
                self.triggerObj.handleRequest(self,message.value)

                if self.stopFlag.is_set():
                    break

        self.listenerObj.close()

if __name__ == "__main__":
    Listener().start()