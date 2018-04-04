import pymongo

def connectMongo():
	host = "127.0.0.1:27017"
	db = "faas"
	collection = "function_topic_mapping"

	url = "mongodb://" + host + "/" + db
	client = pymongo.MongoClient(url)
	db = client[db]
	collection = db[collection]
	return collection

