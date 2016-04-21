from pymongo import MongoClient

if __name__ == '__main__' :
	client = MongoClient("127.0.0.1", 27017)
	mdb = client.episode
	collection = mdb.pltf_basic_info
	for record in collection.find():
		print record
		if len(record) == 2:
			collection.delete_one(record)
		print len(record)
	# print (type(pltfList[1])) #list
	
	
	delete_one()
	insert_one()
	find_one()
