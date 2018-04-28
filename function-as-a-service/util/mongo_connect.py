import pymongo
from config import Config

conf = Config()
def connectMongo():
	host = conf.MONGO_HOSTNAME_PORT
	db = "faas"
	collection = "function_topic_mapping"
	kafka_collection = "kafka_topics_available"
	output_collection = "function_output"

	url = "mongodb://" + host + "/" + db
	client = pymongo.MongoClient(url)
	db = client[db]
	collection = db[collection]
	kafka_collection = db[kafka_collection]
	output_collection = db[output_collection]
	return collection, kafka_collection, output_collection