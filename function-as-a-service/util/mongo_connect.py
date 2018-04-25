import pymongo

def connectMongo():
	host = "127.0.0.1:27017"
	db = "faas"
	collection = "function_topic_mapping"
	kafka_collection = "kafka_topics_available"

	url = "mongodb://" + host + "/" + db
	client = pymongo.MongoClient(url)
	db = client[db]
	collection = db[collection]
	kafka_collection = db[kafka_collection]
	return collection, kafka_collection

