import sys
reload(sys)
sys.setdefaultencoding('utf8')
import web
from multiprocessing import Process, Manager, Lock
import httplib
import json
import time

sum = 0
info = list()
rrh_Version = list()
rrh_SN = list()

class getPltfList(object):
	def __init__(self):
		self.db1 = web.database(dbn='mysql', db = 'episode', user = 'root', pw= 'abc111--', host = '127.0.0.1')
		self.db1.printing = True
		self.db2 = web.database(dbn='mysql', db = 'episode_soc', user = 'root', pw= 'abc111--', host = '127.0.0.1')
		self.db2.printing = True
		self.db3 = web.database(dbn='mysql', db = 'cl_episode', user = 'root', pw= 'abc111--', host = '127.0.0.1')
		self.db3.printing = True
		self.db4 = web.database(dbn='mysql', db = 'cl_episode_soc', user = 'root', pw= 'abc111--', host = '127.0.0.1')
		self.db4.printing = True

	def __call__(self):
		return self.createPltfList()

	def createPltfList(self):
		self.ckb_pltfList = list(self.db1.query('select instant_time, name, ip from EPISODE_INSTANT_INFO order by id DESC'))
		self.cks_pltfList = list(self.db2.query('select instant_time, name, ip from EPISODE_INSTANT_INFO order by id DESC'))
		self.clb_pltfList = list(self.db3.query('select instant_time, name, ip from EPISODE_INSTANT_INFO order by id DESC'))
		self.cls_pltfList = list(self.db4.query('select instant_time, name, ip from EPISODE_INSTANT_INFO order by id DESC'))
		return self.ckb_pltfList, self.cks_pltfList,self.clb_pltfList, self.cls_pltfList

   
class getDataFromMgdb(object):

	def __init__(self):
		self.path = "/home/pc/pltf_basic_jason.txt"#usr/bin/mongoexport -u root -p abc -ddb_name -c collection_name  --jsonArray-f dict1 dict2  -o info_jason.txt将数据导入一个文本并保持键值对的格式

		for line in open(self.path):
			line = str(line).replace("null","None")
			self.info = eval(line)#type:list
	def __call__(self):
		return self.getData()

	def getData(self):
		
		result = dict()
		allInfo = list()

		for record in self.info:
			self.Refresh_Time = record.get('Refresh_Time')
			self.Name = record.get('Cfg').get('Register_Name')
			self.IP = record.get('Cfg').get('Debug_IP')
			self.Site = record.get('Cfg').get('Site')
			self.RRH = record.get('RRH')
			self.D2U_Version = record.get('Conf').get('D2U_Version')
			self.OAM_IP = record.get('Conf').get('OAM_IP')
			self.S1_IP = record.get('Conf').get('S1_IP')
			self.RSI = record.get('Other').get('RSI')
			self.Config = record.get('Other').get('Config')
			self.Frequecny = record.get('Other').get('Frequecny')
			
			self.CCM_Version = record.get('CB').get('CCM_PCB_Ver')	
			self.CCM_Type = record.get('CB').get('Type')	
			self.CCM_Uptime = record.get('CB').get('Uptime')	
			self.CCM_Load = record.get('CB').get('Load_Average')	
			self.CCM_CpuUsage = record.get('CB').get('CPU_Usage')	
			self.CCM_MemUsage = record.get('CB').get('Mem_Usage')

			self.Load_Version = record.get('Status').get('Load_Version')	

			if type(record.get('BB')) == dict:
				if type(record.get('BB').get('BB2')) == dict:
					self.CEM1_Uptime = record.get('BB').get('BB2').get('Uptime')	
					self.CEM1_Load = record.get('BB').get('BB2').get('Load_Average')	
					self.CEM1_CpuUsage = record.get('BB').get('BB2').get('CPU_Usage')	
					self.CEM1_MemUsage = record.get('BB').get('BB2').get('Mem_Usage')
				if type(record.get('BB').get('BB3')) == dict:
					self.CEM2_Uptime = record.get('BB').get('BB3').get('Uptime')	
					self.CEM2_Load = record.get('BB').get('BB3').get('Load_Average')	
					self.CEM2_CpuUsage = record.get('BB').get('BB3').get('CPU_Usage')	
					self.CEM2_MemUsage = record.get('BB').get('BB3').get('Mem_Usage')
				if type(record.get('BB').get('BB4')) == dict:
					self.CEM3_Uptime = record.get('BB').get('BB4').get('Uptime')	
					self.CEM3_Load = record.get('BB').get('BB4').get('Load_Average')	
					self.CEM3_CpuUsage = record.get('BB').get('BB4').get('CPU_Usage')	
					self.CEM3_MemUsage = record.get('BB').get('BB4').get('Mem_Usage')
			else:
				self.CEM1_Uptime = '&nbsp'#None
				self.CEM1_Load = '&nbsp'
				self.CEM1_CpuUsage = '&nbsp'
				self.CEM1_MemUsage = '&nbsp'

				self.CEM2_Uptime = '&nbsp'
				self.CEM2_Load = '&nbsp'
				self.CEM2_CpuUsage = '&nbsp'
				self.CEM2_MemUsage = '&nbsp'


				self.CEM3_Uptime = '&nbsp'
				self.CEM3_Load = '&nbsp'
				self.CEM3_CpuUsage = '&nbsp'
				self.CEM3_MemUsage = '&nbsp'

			del self.RRH['RRH_List']
			rrh_Version =[]
			rrh_SN = []
			for rrh_list in self.RRH:
				rrh_Version.append(dict(self.RRH[rrh_list]).get('Version'))
				rrh_SN.append(dict(self.RRH[rrh_list]).get('Serial_Number'))
			self.RRH_Version = (' ').join(rrh_Version)
			self.RRH_SN = (' ').join(rrh_SN)

			# return self.Refresh_Time,self.Name,self.IP,self.Site,self.D2U_Version,self.OAM_IP,self.S1_IP,self.RRH_Version,self.RRH_SN,self.CCM_Version,self.CCM_Type,self.CCM_Uptime,self.CCM_Load,self.CCM_CpuUsage,self.CCM_MemUsage,self.CEM1_Uptime,self.CEM1_Load,self.CEM1_CpuUsage,self.CEM1_MemUsage,self.CEM2_Uptime,self.CEM2_Load,self.CEM2_CpuUsage,self.CEM2_MemUsage,self.CEM3_Uptime,self.CEM3_Load,self.CEM3_CpuUsage,self.CEM3_MemUsage,self.RRH_Version,self.RRH_SN
			result['Refresh_Time'] = self.Refresh_Time;
			result['Name'] = self.Name
			result['IP'] = self.IP
			result['Site'] = self.Site
			result['D2U_Version'] = self.D2U_Version
			result['OAM_IP'] = self.OAM_IP
			result['S1_IP'] = self.S1_IP
			result['RRH_Version'] = self.RRH_Version
			result['RRH_SN'] = self.RRH_SN
 			result['CCM_Version'] = self.CCM_Version
			result['CCM_Type'] = self.CCM_Type
			result['CCM_Uptime'] = self.CCM_Uptime
			result['CCM_Load'] = self.CCM_Load
			result['CCM_CpuUsage'] = self.CCM_CpuUsage
			result['CCM_MemUsage'] = self.CCM_MemUsage
			result['CEM1_Uptime'] = self.CEM1_Uptime
			result['CEM1_Load'] = self.CEM1_Load
			result['CEM1_CpuUsage'] = self.CEM1_CpuUsage
			result['CEM1_MemUsage'] = self.CEM1_MemUsage

 			result['CEM2_Uptime'] = self.CEM2_Uptime
			result['CEM2_Load'] = self.CEM2_Load
			result['CEM2_CpuUsage'] = self.CEM2_CpuUsage
			result['CEM2_MemUsage'] = self.CEM2_MemUsage

			result['CEM3_Uptime'] = self.CEM3_Uptime
			result['CEM3_Load'] = self.CEM3_Load
			result['CEM3_CpuUsage'] = self.CEM3_CpuUsage
			result['CEM3_MemUsage'] = self.CEM3_MemUsage

			result['Load_Version'] = self.Load_Version
			# print '------result------'
			# print type(result)
			# print 'result'
			allInfo.append(str(result))
			# return '-------allInfo------'
			# print allInfo
			
		return allInfo
			# return (dict)result{'Refresh_Time':self.Refresh_Time}


def judgeEmpty(param):#判断字符是否为空
	if isinstance(param, str):
		return param
	else:
		return ''

def timeFormat(param):
	return time.strptime(param, '%Y-%m-%d %H:%M:%S')

def insertData(element,db):
	db.insert('EPISODE_INSTANT_INFO',instant_time=element.get('Refresh_Time'),rel=element.get('Load_Version')[0:4], name=element.get('Name'), ip=element.get('IP'),rrh_version=element.get('RRH_Version'), d2u_version=element.get('D2U_Version'), oam_ip=element.get('OAM_IP'), s1_ip=element.get('S1_IP'), ccm_version=element.get('CCM_Version'), ccm_type=element.get('CCM_Type'), ccm_uptime=element.get('CCM_Uptime'), ccm_load=element.get('CCM_Load'), ccm_cpuuse=element.get('CCM_CpuUsage'), ccm_memuse=element.get('CCM_MemUsage'), cem1_uptime=element.get('CEM1_Uptime'), cem1_load=element.get('CEM1_Load'), cem1_cpuuse=element.get('CEM1_CpuUsage'), cem1_memuse=element.get('CEM1_MemUsage'),cem2_uptime=element.get('CEM2_Uptime'), cem2_load=element.get('CEM2_Load'), cem2_cpuuse=element.get('CEM2_CpuUsage'), cem2_memuse=element.get('CEM2_MemUsage'),cem3_uptime=element.get('CEM3_Uptime'), cem3_load=element.get('CEM3_Load'), cem3_cpuuse=element.get('CEM3_CpuUsage'), cem3_memuse=element.get('CEM3_MemUsage'), frequency=element.get('Frequency'), rsi=element.get('RSI'))
def updateData(element,db):
	db.query('update EPISODE_INSTANT_INFO set instant_time=\''+ judgeEmpty(element.get('Refresh_Time'))+ '\',rel=\''+judgeEmpty(element.get('Load_Version')[0:4])+'\', rrh_version=\''+ judgeEmpty(element.get('RRH_Version'))+'\', d2u_version=\''+ judgeEmpty(element.get('D2U_Version')) + '\', oam_ip=\''+judgeEmpty(element.get('OAM_IP'))+'\', s1_ip=\''+judgeEmpty(element.get('S1_IP'))+'\', ccm_version=\''+judgeEmpty(element.get('CCM_Version'))+'\', ccm_type=\''+judgeEmpty(element.get('CCM_Type'))+'\', ccm_uptime=\''+judgeEmpty(element.get('CCM_Uptime'))+'\', ccm_load=\''+judgeEmpty(element.get('CCM_Load'))+'\', ccm_cpuuse=\''+judgeEmpty(element.get('CCM_CpuUsage'))+'\', ccm_memuse=\''+judgeEmpty(element.get('CCM_MemUsage'))+'\', cem1_uptime=\''+judgeEmpty(element.get('CEM1_Uptime'))+'\', cem1_load=\''+judgeEmpty(element.get('CEM1_Load'))+'\', cem1_cpuuse=\''+judgeEmpty(element.get('CEM1_CpuUsage'))+'\', cem1_memuse=\''+judgeEmpty(element.get('CEM1_MemUsage'))+'\',cem2_uptime=\''+judgeEmpty(element.get('CEM2_Uptime'))+'\', cem2_load=\''+judgeEmpty(element.get('CEM2_Load'))+'\', cem2_cpuuse=\''+judgeEmpty(element.get('CEM2_CpuUsage'))+'\', cem2_memuse=\''+judgeEmpty(element.get('CEM2_MemUsage'))+'\',cem3_uptime=\''+judgeEmpty(element.get('CEM3_Uptime'))+'\', cem3_load=\''+judgeEmpty(element.get('CEM3_Load'))+'\', cem3_cpuuse=\''+judgeEmpty(element.get('CEM3_CpuUsage'))+'\', cem3_memuse=\''+judgeEmpty(element.get('CEM3_MemUsage'))+'\', frequency=\''+judgeEmpty(element.get('Frequency'))+'\', rsi=\''+judgeEmpty(element.get('RSI'))+'\' where ip=\'' + judgeEmpty(element.get('IP')) + '\' and name=\'' + judgeEmpty(element.get('Name')) + '\'')

if __name__ == '__main__' :
	pltfList = getPltfList()()
	mogdata = getDataFromMgdb()
	db1 = web.database(dbn='mysql', db = 'episode', user = 'root', pw= 'abc111--', host = '127.0.0.1')
	db2 = web.database(dbn='mysql', db = 'episode_soc', user = 'root', pw= 'abc111--', host = '127.0.0.1')
	db3 = web.database(dbn='mysql', db = 'cl_episode', user = 'root', pw= 'abc111--', host = '127.0.0.1')
	db4 = web.database(dbn='mysql', db = 'cl_episode_soc', user = 'root', pw= 'abc111--', host = '127.0.0.1')
	tmp = 1 
	flag = 1
	# print pltfList[0],pltfList[1],pltfList[2],pltfList[3]
	for element in mogdata.getData():
		element = eval(element)
		print element.get('Name'),element.get('IP'),element.get('Refresh_Time'),element.get('Site'),element.get('CCM_Type')
		# print element.get('Load_Version')[0:4]
		if element.get('Site') == 'SH-CK'and element.get('CCM_Type') == 'ECCM2':
			for pltf in pltfList[0]:
				if element.get('Name') == pltf['name'] and element.get('IP') == pltf['ip']:
					flag = 1;
					Instant_time = str(pltf['instant_time'])
					mongo_time =timeFormat(element.get('Refresh_Time'))
					mysql_time = timeFormat(Instant_time)
					if time.mktime(mongo_time) > time.mktime(mysql_time):
						tmp = 1;
						break
					break	
				else:
					tmp = 0
					flag = 0
			if tmp == 0 and flag == 0:
				insertData(element,db1)
			elif tmp == 1 and flag == 1:
				updateData(element,db1)

		elif element.get('Site') == 'SH-CK'and element.get('CCM_Type') == 'BCAM2':
			for pltf in pltfList[1]:
				if element.get('Name') == pltf['name'] and element.get('IP') == pltf['ip']:
					flag = 1;
					Instant_time = str(pltf['instant_time'])
					mongo_time =timeFormat(element.get('Refresh_Time'))
					mysql_time = timeFormat(Instant_time)
					if time.mktime(mongo_time) > time.mktime(mysql_time):
						tmp = 1;
						break
					break	
				else:
					tmp = 0
					flag = 0
			if tmp == 0 and flag == 0:
				insertData(element,db2)
			elif tmp == 1 and flag == 1:
				updateData(element,db2)
		elif element.get('Site') == 'SH-CL'and element.get('CCM_Type') == 'ECCM2':
			for pltf in pltfList[2]:
				if element.get('Name') == pltf['name'] and element.get('IP') == pltf['ip']:
					flag = 1;
					Instant_time = str(pltf['instant_time'])
					mongo_time =timeFormat(element.get('Refresh_Time'))
					mysql_time = timeFormat(Instant_time)
					if time.mktime(mongo_time) > time.mktime(mysql_time):
						tmp = 1;
						break
					break	
				else:
					tmp = 0
					flag = 0
			if tmp == 0 and flag == 0:
				insertData(element,db3)
			elif tmp == 1 and flag == 1:
				updateData(element,db3)
		elif element.get('Site') == 'SH-CL'and element.get('CCM_Type') == 'BCAM2':
			for pltf in pltfList[3]:
				if element.get('Name') == pltf['name'] and element.get('IP') == pltf['ip']:
					flag = 1;
					Instant_time = str(pltf['instant_time'])
					mongo_time =timeFormat(element.get('Refresh_Time'))
					mysql_time = timeFormat(Instant_time)
					if time.mktime(mongo_time) > time.mktime(mysql_time):
						tmp = 1;
						break
					break	
				else:
					tmp = 0
					flag = 0
			if tmp == 0 and flag == 0:
				insertData(element,db4)
			elif tmp == 1 and flag == 1:
				updateData(element,db4)
		else:
			print "Information lack"
			print element.get('Site'),element.get('CCM_Type')


				

		
