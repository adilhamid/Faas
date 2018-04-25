import sys
sys.path.append("..")

from util.mongo_connect import connectMongo

class Database:
	def __init__(self):
		self.collection, self.kafkaCollection = connectMongo()

	def insertFunctionEntry(self, functionName, topicName, f):
		f.save("/tmp/" + functionName + '.py')

		self.collection.update({'functionName': functionName, 'topicName': topicName},
                          {'$set':{'path': "/tmp/"}}, True)

	def updateEntry(self, functionName, f):
		f.save("/tmp/"+functionName+'.py')

		self.collection.update({'functionName': functionName},
                          {'$set':{'path': "/tmp/"}}, True)

	def getDetailsByTopicName(self, topic):
		result = self.collection.find({'topicName': topic})
		return result

	def getAllKafkaTopics(self):
		result = self.kafkaCollection.distinct("kafkaTopic")
		return result

	def getAllFunctionNames(self):
		result = self.collection.distinct("functionName")
		return result

	def getFunctionPath(self, functionName):
		result = self.collection.find({'functionName':functionName})
		return result['path']

	def addKafkaTopic(self, kafkaTopicName):
		self.kafkaCollection.insert({'kafkaTopic': kafkaTopicName})
