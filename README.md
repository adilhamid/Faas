# Function as a service
Run code without thinking about servers. 

## Setting up Kafka locally
For mac, one can install Kafka using following command. Since Kafka is dependent on zookeeper, so zookeeper should be installed before Kafka
```
brew install zookeeper
brew install kafka
```

To run the kafka,
```
brew services start zookeeper
brew services start kafka
```
If that doesn't work, one can try by following commands:
```
zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties 
kafka-server-start /usr/local/etc/kafka/server.properties
```

Kafka Topic creation can be done as follows:
```
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic <topic-name>
```

## Setting up MongoDB locally

Install mongodb according to the operating system you are using. Eg. for MAC, just do
```
brew install mongo
```

Create a data directory in which all mongodb data would reside and give it appropriate permission. By default, mongodb considers /data/db as the path, so you can create at the same path as follows:
``` 
sudo mkdir -p /data/db
``` 
``` 
sudo chmod 0755 /data/db
``` 
Run following command to start the mongo db server
``` 
sudo mongod
``` 
This starts the mongodb server at 127.0.0.1:27017

Run the following command to start the mongodb client:
```
mongo
```
To create the empty database in mongodb, do
```
use faas
```
