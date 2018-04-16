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

		eventDetails = self.database.getDetailsByTopicName(topic)

		print(eventDetails['functionName'])
		print(eventDetails['path'])

		