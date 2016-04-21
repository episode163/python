import sys
reload(sys)
sys.setdefaultencoding('utf8')
import web
import httplib
import json
from pymongo import MongoClient
class getPltfList(object):
	def __init__(self):
		self.db1 = web.database(dbn='mysql', db = 'episode', user = 'root', pw= 'abc111--', host = '127.0.0.1')
		self.db1.printing = False
		self.db2 = web.database(dbn='mysql', db = 'episode_soc', user = 'root', pw= 'abc111--', host = '127.0.0.1')
		self.db2.printing = False
		self.db3 = web.database(dbn='mysql', db = 'cl_episode', user = 'root', pw= 'abc111--', host = '127.0.0.1')
		self.db3.printing = False
		self.db4 = web.database(dbn='mysql', db = 'cl_episode_soc', user = 'root', pw= 'abc111--', host = '127.0.0.1')
		self.db4.printing = False
	def __call__(self):
		return self.createPltfList()

	def createPltfList(self):
		self.ckpltfList = list(self.db1.query('select name, ip from EPISODE_PLTF_INFO order by id DESC'))
		self.ckpltfList += list(self.db2.query('select name, ip from EPISODE_PLTF_INFO order by id DESC'))
		self.clpltfList = list(self.db3.query('select name, ip from EPISODE_PLTF_INFO order by id DESC'))
		self.clpltfList += list(self.db4.query('select name, ip from EPISODE_PLTF_INFO order by id DESC'))

		return self.ckpltfList,self.clpltfList


if __name__ == '__main__' :
	mpList = list()
	flag = 0
	tmp = 0
	sum1 = 0
	sum2 = 0
	pltfList = getPltfList()()
	client = MongoClient("127.0.0.1", 27017)
	mdb = client.episode
	collection = mdb.pltf_basic_info
	# print (type(pltfList[1])) #list
	result= list()
	for pltf_my in pltfList[0]:
		pltf_mog = collection.find()
		for record in pltf_mog:
			IP = record.get('Cfg').get('Debug_IP')
			Name = record.get('Cfg').get('Register_Name')
			# print IP, Name
			if IP == pltf_my['ip']  and Name == pltf_my['name'] :
				flag = 1
				# print IP, Name
				break
			else:
				flag = 0

		if flag == 0 :
			data1 =  {"Cfg" : {"Debug_IP" : pltf_my['ip'],"Register_Name":pltf_my['name'], "Site":"SH-CK"} }
			# print data1
			result.append((data1))
			# collection.insert_one(data1)
			# collection.delete_one(data)
			sum1 = sum1+1
	# print len(result)
	# collection.insert_many(result)
	for pltf_my in pltfList[1]:
		pltf_mog = collection.find()
		for record in pltf_mog:
			IP = record.get('Cfg').get('Debug_IP')
			Name = record.get('Cfg').get('Register_Name')
			if pltf_my['ip'].encode("utf-8")  == IP.encode("utf-8")  and pltf_my['name'].encode("utf-8")  == Name.encode("utf-8") :
				tmp = 1
				# print IP, Name
				break
			else:
				tmp = 0

		if tmp == 0 :
			data2 =  {"Cfg" : {"Debug_IP":pltf_my['ip'],"Register_Name":pltf_my['name'], "Site":"SH-CL"} }
			# print data2
			result.append((data2))

			# collection.insert_one(data2)
			# collection.delete_one(data)
			sum2 = sum2+1

	collection.insert_many(result)


	print sum1,sum2

