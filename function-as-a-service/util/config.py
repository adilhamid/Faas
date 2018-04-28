
class Config:
    def __init__(self):
        self.KAFKA_QUEUE_HOSTNAME_PORT = "kafkaserver:9092"  ## localhost kafkaserver
        self.MONGO_HOSTNAME_PORT = "mongo:27017" # 127.0.0.1
        self.ADMIN_WEBAPP_HOSTNAME = "http://localhost" ## http://localhost:63342/689-18-a-P2/webapp/

        #
        self.INSTANCE = "ec2-user@ec2-34-205-18-19.compute-1.amazonaws.com"