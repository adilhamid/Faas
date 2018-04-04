import sys
sys.path.append("..")

from util.mongo_connect import connectMongo

class Database:
	def __init__(self):
		self.collection = connectMongo()

	def insertFunctionEntry(self, functionName, topicName, f):
		f.save("/tmp/" + functionName)

		self.collection.update({'functionName': functionName, 'topicName': topicName},
                          {'$set':{'path': "/tmp/" + functionName}}, True)