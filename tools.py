#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-

import re

class Tools:
	def __init__(self):
		self.fout=0
		self.mid_fout=0
		self.count=0
		self.address=99
		self.InterCode=dict()
		self.truelist=[]
		self.falselist=[]
		self.alive_table=dict()
		self.RVALUE=dict()
		self.AVALUE=dict()
		self.Lable=dict()
		#self.Free_reg=[0]

	#def __del__(self):
	#	self.fout.write("\nreal_end:")
	#	self.fout.close()

	def open_file(self,out_asm_file,out_mid_file):
		self.fout=open(out_asm_file,'w')
		self.mid_fout=open(out_mid_file,'w')

	def show_error(self,current):
		global code_line
		print("--------------------------------------------------")
		print((" %d         " %(current-1))+code_line[current-2])
		print((" %d       >>" %(current))+code_line[current-1])
		print((" %d         " %(current+1))+code_line[current])

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
		tempName='_T'+str(self.count)
		self.count+=1
		return tempName

	def code_block(self):
		base_block=[]
		start_address=[]
		end_address=[]
		for key in self.InterCode:
			if self.InterCode[key][0]=='enter':
				start_address.append(key)
			elif self.InterCode[key][0]=='ret':
				end_address.append(key)
			if self.InterCode[key][0][0]=='j':
				end_address.append(key)
				start_address.append(key+1)
				start_address.append(int(self.InterCode[key][3]))

		start_address=list(set(start_address))
		start_address.sort()
		end_address.sort()
		#print(start_address)
		#print(end_address)

		i=0
		j=0
		while True:
			if i<len(start_address) and j<len(end_address):
				if start_address[i]<=end_address[j]:
					base_block.append([start_address[i],'s'])
					i+=1
				else:
					base_block.append([end_address[j],'e'])
					j+=1

			elif i>=len(start_address) and j<len(end_address):
				base_block.append([end_address[j],'e'])
				j+=1

			elif i<len(start_address) and j>=len(end_address):
				base_block.append([start_address[i],'s'])
				i+=1
			else:
				break

		#print(base_block)

		alive_table=dict()
		i=0
		while True:
			start=base_block[i][0]
			i+=1
			if i>=len(base_block):
				end=start
			elif base_block[i][1]=='s':
				end=base_block[i][0]-1
			else:		
				end=base_block[i][0]
				i+=1

			varr=dict()
			for j in range(start,end+1):
				code=','.join(self.InterCode[j])
				#print(str(j)+':'+code)
				self.mid_fout.write((str(j)+':'+code)+'\n')
				for k in range(1,4):
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',self.InterCode[j][k])!=None:
						varr[self.InterCode[j][k]]=['^','^']
			#print('-------------------')
			self.mid_fout.write('-------------------\n')

			#print(varr)

			for j in range(end,start-1,-1):
				#print(j)
				#print(alive_table)
				if self.InterCode[j][0][0]=='j':
					lop=self.InterCode[j][1]
					if lop=='-':
						alive_table[j]=[['^','^'],['^','^'],['^','^']]
					else:	
						alive_table[j]=[varr[lop],['^','^'],['^','^']]
						varr[lop]=[j,'y']
				elif self.InterCode[j][0]=='enter' or self.InterCode[j][0]=='ret' or self.InterCode[j][0]=='call':
					alive_table[j]=[['^','^'],['^','^'],['^','^']]
				elif self.InterCode[j][0]==':=':
					lop=self.InterCode[j][1]
					lvr=self.InterCode[j][3]
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None:
						alive_table[j]=[varr[lvr],['^','^'],['^','^']]
					else:
						alive_table[j]=[varr[lvr],varr[lop],['^','^']]
					varr[lvr]=['^','^']
					varr[lop]=[j,'y']
				else:
					lop=self.InterCode[j][1]
					rop=self.InterCode[j][2]
					lvr=self.InterCode[j][3]
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None and re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',rop)==None:
						alive_table[j]=[varr[lvr],['^','^'],['^','^']]
						varr[lvr]=['^','^']
					elif re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None:
						alive_table[j]=[varr[lvr],['^','^'],varr[rop]]
						varr[rop]=['^','^']
						varr[lvr]=['^','^']
					elif re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',rop)==None:
						alive_table[j]=[varr[lvr],varr[lop],['^','^']]
						varr[lvr]=['^','^']
						varr[lop]=[j,'y']
					else:
						alive_table[j]=[varr[lvr],varr[lop],varr[rop]]
						varr[rop]=['^','^']
						varr[lvr]=['^','^']
						varr[lop]=[j,'y']


			if i>=len(base_block):
				break

		count=0
		for key in self.InterCode:
			if self.InterCode[key][0][0]=='j':
				addr=self.InterCode[key][3]
				self.Lable[addr]='Target'+str(count)
				count+=1

		#print(alive_table)
		#print(self.Lable)
		self.mid_fout.close()
		self.alive_table=alive_table

	def request_reg(self,temp_val):
		if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',temp_val)==None:
			for i in range(10):
				flag=self.RVALUE.get(i)
				if flag==None:
					return i
		else:
			flag=self.AVALUE.get(temp_val)
			if flag==None:
				self.AVALUE[temp_val]=[]
				for i in range(10):
					flag2=self.RVALUE.get(i)
					if flag2==None:
						self.RVALUE[i]=temp_val
						self.AVALUE[temp_val].append(i)
						return i

				#self.RVALUE.pop(0)
				#self.AVALIE[temp_val]
			else:
				return flag[0]

	def free_reg(self,key,no):
		temp_val=self.InterCode[key][no]
		temp_info=self.alive_table[key][no]
		flag=self.AVALUE.get(temp_val)
		if flag!=None:
			if temp_info[1]=='^':
				for i in range(len(flag)):
					self.RVALUE.pop(flag[i])
				self.AVALUE.pop(temp_val)

	def preface(self):
		self.fout.write("lui $sp 0x8000"+'\n')
		self.fout.write("addiu $sp $sp 0x0000"+'\n')
		self.fout.write("move $fp $sp"+'\n')
		self.fout.write("start:"+'\n')
		self.fout.write("lui $ra 0x0040"+'\n')
		self.fout.write("addiu $ra $ra 0x001c"+'\n')
		self.fout.write("j main"+'\n')
		self.fout.write("nop"+'\n')
		self.fout.write("end:"+'\n')
		self.fout.write("j real_end"+'\n')
		self.fout.write("nop"+'\n\n')

	def make_code(self,symbol_table,fun_name_table):
		self.preface()
		base_address=0x00400000		#内存起始地址
		now_address=0x00400000
		for key in self.InterCode:
			mcode=self.InterCode[key]
			flag=self.Lable.get(str(key))
			if flag!=None:
				#print("%s :" %flag)
				self.fout.write(("%s :" %flag)+'\n')

			if mcode[0]=='enter':
				fun_id=int(mcode[1])
				fun_name=fun_name_table[fun_id]
				frame_size=symbol_table[fun_name].frame_size
				symbol_table[fun_name].enter_address=key 
				#print(fun_name+":")
				self.fout.write(fun_name+":"+'\n')
				#print("addiu $sp $sp -%d" %frame_size)
				self.fout.write(("addiu $sp $sp -%d" %frame_size)+'\n')
				#print("sw $ra %d($sp)" %(frame_size-4))
				self.fout.write(("sw $ra %d($sp)" %(frame_size-4))+'\n')
				#print("sw $fp %d($sp)" %(frame_size-8))
				self.fout.write(("sw $fp %d($sp)" %(frame_size-8))+'\n')
				#print("move $fp $sp")
				self.fout.write(("move $fp $sp")+'\n')

				for i in range(len(symbol_table[fun_name].formal_table)):
					#print("sw $a%d %d($fp)" %(i,(frame_size+i*4)))
					self.fout.write(("sw $a%d %d($fp)" %(i,(frame_size+i*4)))+'\n')
					now_address+=4

			elif mcode[0]=='ret':
				#print("move $sp $fp")
				self.fout.write(("move $sp $fp")+'\n')
				#print("lw $fp %d($sp)" %(frame_size-8))
				self.fout.write(("lw $fp %d($sp)" %(frame_size-8))+'\n')
				#print("lw $ra %d($sp)" %(frame_size-4))
				self.fout.write(("lw $ra %d($sp)" %(frame_size-4))+'\n')
				#print("jr $ra")
				self.fout.write(("jr $ra")+'\n')
				#print("addiu $sp $sp %d" %frame_size)
				self.fout.write(("addiu $sp $sp %d" %frame_size)+'\n')

			elif mcode[0]=='call':
				#print("jal %s" %mcode[1])
				self.fout.write(("jal %s" %mcode[1])+'\n')
				#print("nop")
				self.fout.write(("nop")+'\n')

			elif mcode[0]=='j':
				#print("j %s" %(self.Lable[mcode[3]]))
				self.fout.write(("j %s" %(self.Lable[mcode[3]]))+'\n')
				#print("nop")
				self.fout.write(("nop")+'\n')

			elif mcode[0]=='j>':
				lop=mcode[1]
				rop=mcode[2]
				if mcode[1][0]!='_' and mcode[2][0]!='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None:
						reg1=self.request_reg(lop)
						#print("li $t%d %d" %(reg1,int(lop)))
						self.fout.write(("li $t%d %d" %(reg1,int(lop)))+'\n')
					else:
						reg1=self.request_reg(lop)
						#print("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))+'\n')
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',rop)==None:
						reg2=self.request_reg(rop)
						#print("li $t%d %d" %(reg2,int(rop)))
						self.fout.write(("li $t%d %d" %(reg2,int(rop)))+'\n')
					else:
						reg2=self.request_reg(rop)
						#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')

					#print("bgt $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("bgt $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				elif mcode[1][0]!='_' and mcode[2][0]=='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None:
						reg1=self.request_reg(lop)
						#print("li $t%d %d" %(reg1,int(lop)))
						self.fout.write(("li $t%d %d" %(reg1,int(lop)))+'\n')
					else:
						reg1=self.request_reg(lop)
						#print("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))+'\n')

					reg2=self.request_reg(rop)
					#print("bgt $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("bgt $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				elif mcode[1][0]=='_' and mcode[2][0]!='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',rop)==None:
						reg2=self.request_reg(rop)
						#print("li $t%d %d" %(reg2,int(rop)))
						self.fout.write(("li $t%d %d" %(reg2,int(rop)))+'\n')
					else:
						reg2=self.request_reg(rop)
						#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')

					reg1=self.request_reg(lop)
					#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
					self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')
					#print("bgt $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("bgt $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				else:
					reg1=self.request_reg(lop)
					reg2=self.request_reg(rop)
					#print("bgt $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("bgt $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				#print("nop")
				self.fout.write(("nop")+'\n')

			elif mcode[0]=='j>=':
				lop=mcode[1]
				rop=mcode[2]
				if mcode[1][0]!='_' and mcode[2][0]!='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None:
						reg1=self.request_reg(lop)
						#print("li $t%d %d" %(reg1,int(lop)))
						self.fout.write(("li $t%d %d" %(reg1,int(lop)))+'\n')
					else:
						reg1=self.request_reg(lop)
						#print("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))+'\n')
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',rop)==None:
						reg2=self.request_reg(rop)
						#print("li $t%d %d" %(reg2,int(rop)))
						self.fout.write(("li $t%d %d" %(reg2,int(rop)))+'\n')
					else:
						reg2=self.request_reg(rop)
						#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')

					#print("bge $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("bge $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				elif mcode[1][0]!='_' and mcode[2][0]=='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None:
						reg1=self.request_reg(lop)
						#print("li $t%d %d" %(reg1,int(lop)))
						self.fout.write(("li $t%d %d" %(reg1,int(lop)))+'\n')
					else:
						reg1=self.request_reg(lop)
						#print("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))+'\n')

					reg2=self.request_reg(rop)
					#print("bge $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("bge $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				elif mcode[1][0]=='_' and mcode[2][0]!='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',rop)==None:
						reg2=self.request_reg(rop)
						#print("li $t%d %d" %(reg2,int(rop)))
						self.fout.write(("li $t%d %d" %(reg2,int(rop)))+'\n')
					else:
						reg2=self.request_reg(rop)
						#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')
						
					reg1=self.request_reg(lop)
					#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
					self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')
					#print("bge $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("bge $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				else:
					reg1=self.request_reg(lop)
					reg2=self.request_reg(rop)
					#print("bge $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("bge $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				#print("nop")
				self.fout.write(("nop")+'\n')

			elif mcode[0]=='j<':
				lop=mcode[1]
				rop=mcode[2]
				if mcode[1][0]!='_' and mcode[2][0]!='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None:
						reg1=self.request_reg(lop)
						#print("li $t%d %d" %(reg1,int(lop)))
						self.fout.write(("li $t%d %d" %(reg1,int(lop)))+'\n')
					else:
						reg1=self.request_reg(lop)
						#print("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))+'\n')
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',rop)==None:
						reg2=self.request_reg(rop)
						#print("li $t%d %d" %(reg2,int(rop)))
						self.fout.write(("li $t%d %d" %(reg2,int(rop)))+'\n')
					else:
						reg2=self.request_reg(rop)
						#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')

					#print("blt $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("blt $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				elif mcode[1][0]!='_' and mcode[2][0]=='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None:
						reg1=self.request_reg(lop)
						#print("li $t%d %d" %(reg1,int(lop)))
						self.fout.write(("li $t%d %d" %(reg1,int(lop)))+'\n')
					else:
						reg1=self.request_reg(lop)
						#print("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))+'\n')

					reg2=self.request_reg(rop)
					#print("blt $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("blt $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				elif mcode[1][0]=='_' and mcode[2][0]!='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',rop)==None:
						reg2=self.request_reg(rop)
						#print("li $t%d %d" %(reg2,int(rop)))
						self.fout.write(("li $t%d %d" %(reg2,int(rop)))+'\n')
					else:
						reg2=self.request_reg(rop)
						#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')
						
					reg1=self.request_reg(lop)
					#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
					self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')
					#print("blt $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("blt $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				else:
					reg1=self.request_reg(lop)
					reg2=self.request_reg(rop)
					#print("blt $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("blt $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				#print("nop")
				self.fout.write(("nop")+'\n')


			elif mcode[0]=='j<=':
				lop=mcode[1]
				rop=mcode[2]
				if mcode[1][0]!='_' and mcode[2][0]!='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None:
						reg1=self.request_reg(lop)
						#print("li $t%d %d" %(reg1,int(lop)))
						self.fout.write(("li $t%d %d" %(reg1,int(lop)))+'\n')
					else:
						reg1=self.request_reg(lop)
						#print("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))+'\n')
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',rop)==None:
						reg2=self.request_reg(rop)
						#print("li $t%d %d" %(reg2,int(rop)))
						self.fout.write(("li $t%d %d" %(reg2,int(rop)))+'\n')
					else:
						reg2=self.request_reg(rop)
						#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')

					#print("ble $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("ble $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				elif mcode[1][0]!='_' and mcode[2][0]=='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None:
						reg1=self.request_reg(lop)
						#print("li $t%d %d" %(reg1,int(lop)))
						self.fout.write(("li $t%d %d" %(reg1,int(lop)))+'\n')
					else:
						reg1=self.request_reg(lop)
						#print("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))+'\n')

					reg2=self.request_reg(rop)
					#print("ble $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("ble $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				elif mcode[1][0]=='_' and mcode[2][0]!='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',rop)==None:
						reg2=self.request_reg(rop)
						#print("li $t%d %d" %(reg2,int(rop)))
						self.fout.write(("li $t%d %d" %(reg2,int(rop)))+'\n')
					else:
						reg2=self.request_reg(rop)
						#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')
						
					reg1=self.request_reg(lop)
					#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
					self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')
					#print("ble $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("ble $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				else:
					reg1=self.request_reg(lop)
					reg2=self.request_reg(rop)
					#print("ble $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("ble $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				#print("nop")
				self.fout.write(("nop")+'\n')

			elif mcode[0]=='j==':
				lop=mcode[1]
				rop=mcode[2]
				if mcode[1][0]!='_' and mcode[2][0]!='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None:
						reg1=self.request_reg(lop)
						#print("li $t%d %d" %(reg1,int(lop)))
						self.fout.write(("li $t%d %d" %(reg1,int(lop)))+'\n')
					else:
						reg1=self.request_reg(lop)
						#print("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))+'\n')
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',rop)==None:
						reg2=self.request_reg(rop)
						#print("li $t%d %d" %(reg2,int(rop)))
						self.fout.write(("li $t%d %d" %(reg2,int(rop)))+'\n')
					else:
						reg2=self.request_reg(rop)
						#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')

					#print("beq $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("beq $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				elif mcode[1][0]!='_' and mcode[2][0]=='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None:
						reg1=self.request_reg(lop)
						#print("li $t%d %d" %(reg1,int(lop)))
						self.fout.write(("li $t%d %d" %(reg1,int(lop)))+'\n')
					else:
						reg1=self.request_reg(lop)
						#print("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))+'\n')

					reg2=self.request_reg(rop)
					#print("beq $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("beq $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				elif mcode[1][0]=='_' and mcode[2][0]!='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',rop)==None:
						reg2=self.request_reg(rop)
						#print("li $t%d %d" %(reg2,int(rop)))
						self.fout.write(("li $t%d %d" %(reg2,int(rop)))+'\n')
					else:
						reg2=self.request_reg(rop)
						#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')
						
					reg1=self.request_reg(lop)
					#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
					self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')
					#print("beq $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("beq $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				else:
					reg1=self.request_reg(lop)
					reg2=self.request_reg(rop)
					#print("beq $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("beq $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				#print("nop")
				self.fout.write(("nop")+'\n')


			elif mcode[0]=='j!=':
				lop=mcode[1]
				rop=mcode[2]
				if mcode[1][0]!='_' and mcode[2][0]!='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None:
						reg1=self.request_reg(lop)
						#print("li $t%d %d" %(reg1,int(lop)))
						self.fout.write(("li $t%d %d" %(reg1,int(lop)))+'\n')
					else:
						reg1=self.request_reg(lop)
						#print("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))+'\n')
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',rop)==None:
						reg2=self.request_reg(rop)
						#print("li $t%d %d" %(reg2,int(rop)))
						self.fout.write(("li $t%d %d" %(reg2,int(rop)))+'\n')
					else:
						reg2=self.request_reg(rop)
						#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')

					#print("bne $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("bne $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				elif mcode[1][0]!='_' and mcode[2][0]=='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None:
						reg1=self.request_reg(lop)
						#print("li $t%d %d" %(reg1,int(lop)))
						self.fout.write(("li $t%d %d" %(reg1,int(lop)))+'\n')
					else:
						reg1=self.request_reg(lop)
						#print("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))+'\n')

					reg2=self.request_reg(rop)
					#print("bne $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("bne $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				elif mcode[1][0]=='_' and mcode[2][0]!='_':
					if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',rop)==None:
						reg2=self.request_reg(rop)
						#print("li $t%d %d" %(reg2,int(rop)))
						self.fout.write(("li $t%d %d" %(reg2,int(rop)))+'\n')
					else:
						reg2=self.request_reg(rop)
						#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
						self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')
						
					reg1=self.request_reg(lop)
					#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
					self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')
					#print("bne $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("bne $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				else:
					reg1=self.request_reg(lop)
					reg2=self.request_reg(rop)
					#print("bne $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))
					self.fout.write(("bne $t%d $t%d %s" %(reg1,reg2,self.Lable[mcode[3]]))+'\n')
					self.free_reg(key,1)
					self.free_reg(key,2)

				#print("nop")
				self.fout.write(("nop")+'\n')


			elif mcode[0]==':=':
				lvr=mcode[3]
				lop=mcode[1]
				
				if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None:	#左操作是个立即数
					if lvr[0]!='_':
						reg=self.request_reg(lop)
						#print("li $t%d %d" %(reg,int(lop)))
						self.fout.write(("li $t%d %d" %(reg,int(lop)))+'\n')
						#print("sw $t%d %d($fp)" %(reg,symbol_table[fun_name].frame_temp_sp[lvr]))
						self.fout.write(("sw $t%d %d($fp)" %(reg,symbol_table[fun_name].frame_temp_sp[lvr]))+'\n')
					else:
						#print("li $%s %d" %(lvr[1:len(lvr)],int(lop)))
						self.fout.write(("li $%s %d" %(lvr[1:len(lvr)],int(lop)))+'\n')
					#self.free_reg(key,1)
				elif lvr[0]!='_' and lop[1]=='T':									#左值是局部变量
					reg=self.request_reg(lop)
					#print("sw $t%d %d($fp)" %(reg,symbol_table[fun_name].frame_temp_sp[lvr]))
					self.fout.write(("sw $t%d %d($fp)" %(reg,symbol_table[fun_name].frame_temp_sp[lvr]))+'\n')
					self.free_reg(key,1)

				elif lvr[0]!='_' and lop[1]!='T':											#左值是内部变量
					#print("sw $%s %d($fp)" %(lop[1:len(lop)],symbol_table[fun_name].frame_temp_sp[lvr]))
					self.fout.write(("sw $%s %d($fp)" %(lop[1:len(lop)],symbol_table[fun_name].frame_temp_sp[lvr]))+'\n')

				elif lvr[0]=='_':
					if lop[0]=='_':
						if lop[1]=='T':
							reg=self.request_reg(lop)
							#print("move $%s $t%d " %(lvr[1:len(lvr)],reg))
							self.fout.write(("move $%s $t%d " %(lvr[1:len(lvr)],reg))+'\n')
							self.free_reg(key,1)
						else:
							reg=self.request_reg(lvr)
							#print("move $t%d %s" %(reg,lop[1:len(lvr)]))
							self.fout.write(("move $t%d %s" %(reg,lop[1:len(lvr)]))+'\n')
							self.free_reg(key,2)
					else:
						if lvr[1]=='T':
							reg=self.request_reg(lvr)
							#print("lw $t%d %d($fp)" %(reg,symbol_table[fun_name].frame_temp_sp[lop]))
							self.fout.write(("lw $t%d %d($fp)" %(reg,symbol_table[fun_name].frame_temp_sp[lop]))+'\n')
							self.free_reg(key,2)
						else:
							#print("lw $%s %d($fp)" %(lvr[1:len(lvr)],symbol_table[fun_name].frame_temp_sp[lop]))
							self.fout.write(("lw $%s %d($fp)" %(lvr[1:len(lvr)],symbol_table[fun_name].frame_temp_sp[lop]))+'\n')


				#elif lvr[0]=='_' and lop[1]!='T':
				#	print("lw $%s %d($fp)" %(lvr[1:len(lvr)-1],symbol_table[fun_name].frame_temp_sp[lop]))


			elif mcode[0]=='+' or mcode[0]=='-' or mcode[0]=='*' or mcode[0]=='/':
				lop=mcode[1]
				rop=mcode[2]
				lvr=mcode[3]

				if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',lop)==None:	
					reg1=self.request_reg(lop)
					#print("li $t%d %d" %(reg1,int(lop)))
					self.fout.write(("li $t%d %d" %(reg1,int(lop)))+'\n')
				elif lop[0]=='_':
					reg1=self.request_reg(lop)
				else:
					reg1=self.request_reg(lop)
					#print("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))
					self.fout.write(("lw $t%d %d($fp)" %(reg1,symbol_table[fun_name].frame_temp_sp[lop]))+'\n')

				if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',rop)==None:	
					reg2=self.request_reg(rop)
					#print("li $t%d %d" %(reg2,int(rop)))
					self.fout.write(("li $t%d %d" %(reg2,int(rop)))+'\n')
				elif rop[0]=='_':
					reg2=self.request_reg(rop)
				else:
					reg2=self.request_reg(rop)
					#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))
					self.fout.write(("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))+'\n')
					#print(mcode)
					#print(reg1,reg2,rop)
					#print(self.RVALUE)
					#print(self.AVALUE)
					#print("lw $t%d %d($fp)" %(reg2,symbol_table[fun_name].frame_temp_sp[rop]))

				reg3=self.request_reg(lvr)

				if mcode[0]=='+':
					#print("addu $t%d $t%d $t%d" %(reg3,reg1,reg2))
					self.fout.write(("addu $t%d $t%d $t%d" %(reg3,reg1,reg2))+'\n')
				elif mcode[0]=='-':
					#print("subu $t%d $t%d $t%d" %(reg3,reg1,reg2))
					self.fout.write(("subu $t%d $t%d $t%d" %(reg3,reg1,reg2))+'\n')
				elif mcode[0]=='*':
					#print("mul $t%d $t%d $t%d" %(reg3,reg1,reg2))
					self.fout.write(("mul $t%d $t%d $t%d" %(reg3,reg1,reg2))+'\n')
					#print("move $t%d lo" %(reg3))
				elif mcode[0]=='/':
					#print("div $t%d $t%d $t%d" %(reg3,reg1,reg2))
					self.fout.write(("div $t%d $t%d $t%d" %(reg3,reg1,reg2))+'\n')
					#print("move $t%d lo" %(reg3))

				self.free_reg(key,0)
				self.free_reg(key,1)
				self.free_reg(key,2)

		self.fout.write("\nreal_end:")
		self.fout.close()

				


















#def make_code(alive_table):






