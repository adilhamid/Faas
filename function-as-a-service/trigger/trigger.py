from database import Database
from resourceManager import ResourceManager

class Trigger:
	def __init__(self):
		self.resourceManager = ResourceManager()
		self.database = Database()

	def handleRequest(self, payload):
		source_lambda_id = payload["source_lambda_id"]

		eventDetails = self.database.findBySourceLambdaId(source_lambda_id)

		