from elasticsearch import Elasticsearch

class Database:
	def __init__(self):
		self.es = Elasticsearch()
		self.es.indices.create(index='lambda-mappings', ignore=400)

	def findBySourceLambdaId(self, id):
		self.get(index="lambda-mappings", doc_type="mappings", id=42)['_source']