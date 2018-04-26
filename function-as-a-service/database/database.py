import sys
import os
import subprocess
sys.path.append("..")

from util.mongo_connect import connectMongo

class Database:
	def __init__(self):
		self.collection, self.kafkaCollection, self.outputCollection = connectMongo()


	def checkPythonFile(self, filePath):

		# Check the file is compilable
		command = "pyflakes " + filePath + " > output.log 2>&1"

		try:
			subprocess.check_output(command, shell=True)
		except subprocess.CalledProcessError as e:
			print e
			raise Exception(e.message)

		command = "rm output.log"
		try:
			fileSize = os.stat("output.log").st_size
			subprocess.check_output(command, shell=True)

			if fileSize >0:
				return False
			else:
				return True

		except:
			print "Problem while checking the output.log file"
			raise Exception("Problem Opening or removing the output.log")



	def insertFunctionEntry(self, functionName, topicName, f):
		filePath = "/tmp/" + functionName + '.py'
		f.save(filePath)

		if self.checkPythonFile(filePath):

			self.collection.update({'functionName': functionName, 'topicName': topicName},
                          {'$set':{'path': "/tmp/"}}, True)
		else:
			command  = "rm "+filePath
			try:
				subprocess.check_output(command, shell=True)
			except:
				print "Problem deleting the saved file"

	def updateEntry(self, functionName, f):
		filePath = "/tmp/" + functionName + '.py'
		f.save(filePath)

		if self.checkPythonFile(filePath):
			self.collection.update({'functionName': functionName},
								   {'$set': {'path': "/tmp/"}}, True)
		else:
			command = "rm " + filePath
			try:
				subprocess.check_output(command, shell=True)
			except:
				print "Problem deleting the saved file"

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

	def getAllFunctionOutputs(self):
		result = self.outputCollection.find()
		return result

	def insertFunctionOutput(self, functionName, userData, output, timestamp):
		self.outputCollection.insert({'timestamp' : timestamp,'functionName': functionName, 'userData': userData,
							   	'outputResult': output})

