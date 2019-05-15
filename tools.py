#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-

class Tools:
	def __init__(self):
		self.fout=open("test.out",'w')
		self.count=0
		self.address=99
		self.InterCode=dict()
		self.truelist=[]
		self.falselist=[]

	def __del__(self):
		self.fout.close()

	def emit(self,s1,s2,s3,s4):
		#fout.write(s)
		#fout.write('\r\n')
		self.address+=1
		self.InterCode[self.address]=[s1,s2,s3,s4]
		return self.address

	def makelist(self):
		self.truelist.clear()
		self.falselist.clear()

	def backpatch(self,addr,jump):
		self.InterCode[addr][3]=str(jump)


	def nextquad(self):
		return self.address+1

	def show_me_code(self):
		for key in self.InterCode:
			code=','.join(self.InterCode[key])
			print(str(key)+':'+code)

	def newTemp(self):
		tempName='T'+str(self.count)
		self.count+=1
		return tempName
