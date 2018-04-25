import sys

sys.path.append("..")
from database.database import Database
from resourceManager.resourceManager import ResourceManager

class Trigger:
	def __init__(self):
		self.resourceManager = ResourceManager()
		self.database = Database()

	def handleRequest(self, payload):
		topic = payload.topic
		message = payload.value

		functionDetails = self.database.getDetailsByTopicName(topic)

		for detail in functionDetails:
			self.resourceManager.executeLambda(detail['path'], detail['functionName'], message)