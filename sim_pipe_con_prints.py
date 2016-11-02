import sys
import datetime
import bitstring

### DEFINICION DE VARIABLES GLOBALES ####
ARREGLO = [0] * 5000
PC = 0
LIMITE = 0
instructions_type= {
	'add':'R',
	'addi':'I',
	'mul':'R',
	'j':'J',
	'beq':'I',
	'blt':'I',
	'bgt':'I',
	'nop':'R',
	'div':'R',
	'mflo':'R',
	'mfhi':'R',
	'lw':'I',
	'sw':'I',
	'la':'I',
	}
instructions_opcode= {
	'add':'000000',
	'mul':'000000',
	'nop': '000000' ,
	'div': '000000',
	'mflo':'000000',
	'mfhi':'000000',
	'j':'000010',
	'beq':'000100',
	'addi':'001000',
	'lw':'100011',
	'sw':'101011',
	'blt':'111100',
	'bgt':'111110',
	'la':'111111'
	}
funct = {
	'add':'010100',
	'mul':'000000',
	'nop': '000000' ,
	'div': '011010',
	'mflo':'001100',
	'mfhi':'001010',
	'addi':'000001',
	'lw':  '000010',
	'sw':  '000011',
	'beq': '000100',
	'blt': '000101',
	'bgt': '000110',
	'la':  '000111',
	'j': '001000'
	}
alu_operations = {
	'010100':'0000', #add
	'000000':'0001', #mul
	'000000':'0010', #nop
	'011010':'0011', #div
	'001100':'0100', #mflo
	'001010':'0101', #mfhi
	'000001':'0110', #addi
	'000010':'0111', #lw
	'000011':'1000', #sw
	'000100':'1001', #beq
	'000101':'1010', #blt
	'000110':'1011', #bgt
	'000111':'1100', #la
	'001000':'1101' #j
	}
registers = {
	'$zero': '00000',
	'$v0': '00001',
	'$v1': '00010',
	'$a': '00011',
	'$a1': '00100',
	'$a2': '00101',
	'$a3': '00110',
	'$t0': '00111',
	'$t1': '01000',
	'$t2': '01001',
	'$t3': '01010',
	'$t4': '01011',
	'$t5': '01100',
	'$t6': '01101',
	'$t7': '01110',
	'$t8': '01111',
	'$t9': '10000',
	'lo': '10001',
	'hi': '10010'
	}
R = {
	'00000': 0,
	'00001': 0,
	'00010': 0,
	'00011': 0,
	'00100': 0,
	'00101': 0,
	'00110': 0,
	'00111': 0,
	'01000': 0,
	'01001': 0,
	'01010': 0,
	'01011': 0,
	'01100': 0,
	'01101': 0,
	'01110': 0,
	'01111': 0,
	'10000': 0,
	'10001': 0,
	'10010': 0
	}
CONTROL_UNIT = {
	'RegDst':0,
	'Branch':0,
	'MemRead':0,
	'MemtoReg':0,
	'ALUOp1':0,
	'ALUOp2':0,
	'MemWrite':0,
	'ALUSrc':0,
	'RegWrite':0
	}
muxes = {'RegDst': 0, 'ALUSrc': 0, 'MemtoReg': 0,'PCSrc': 0}
ALU_CONTROL_UNIT = {'ALUControlOut': ''}
REGISTROS = {
	'ReadReg1': '',
	'ReadReg2': '',
	'WriteReg': '',
	'WriteData': 0,
	'ReadData1': 0,
	'ReadData2': 0
	}
instructions_memory = []
#Buffer para IF/ID contiene [intruccion_word_32_bits,PC+4]
IF_ID = {
	'Instruction': '',
	'PC+4':0
	}
#Buffer para ID/EX contiene [PC+4,Branch,MemRead,MemtoReg,MemWrite,ALUOp,ALUSrc,
#							RegWrite,ReadData1,ReadData2,sign_extend(immediate),
#							funct,rt,rd,RegDst]
ID_EX = {
	'PC+4':0,
	'Branch':0,
	'MemRead':0,
	'MemtoReg':0,
	'MemWrite':0,
	'ALUOp1':0,
	'ALUOp2':0,
	'ALUSrc':0,
	'RegWrite':0,
	'ReadData1':0,
	'ReadData2':0,
	'Sign-extend_imm':'',
	'Funct':'',
	'Rt':'',
	'Rd':'',
	'RegDst':0
	}
#Buffer para EX/MEM contiene [Add_result, lineas de control, Zero, ALU_Result, 
#								ReadData2,MUXRegDst_result]
EX_MEM = {
	'Add_result':0,
	'Branch':0,
	'MemRead':0,
	'MemtoReg':0,
	'MemWrite':0,
	'RegWrite':0,
	'ReadData2':0,
	'Zero': 0,
	'ALU_Output':0,
	'MUXRegDst_Output':''
	}
#Buffer para MEM/WB contiene [MemtoReg,RegWrite,ReadData,ALU_Result,MUXRegDst_Output]
MEM_WB = {
	'MemtoReg':0,
	'RegWrite':0,
	'ReadData':0,
	'ALU_Output':0,
	'MUXRegDst_Output':''
	}
ALU = {
	'A':0,
	'B':0,
	'Result':0,
	'Zero':0,
	'Control':''
	}
DATA_MEMORY = {
	'ReadData': 0
	}


### IMPORTACION DE FUNCIONES Y CLASES####

### IMPLENTACION O DEFINICION DE FUNCIONES Y ClASES###
def get_register_code(reg):
	if reg:
		return registers[reg]

def get_instruction_type(mnemonic):
	if mnemonic:
		instruction_name = mnemonic
		if instructions_type.has_key(instruction_name):
			if instruction_name == 'add':
				return instructions_type['add']
			elif instruction_name == 'addi':
				return instructions_type['addi']
			elif instruction_name == 'mul':
				return instructions_type['mul']
			elif instruction_name == 'j':
				return instructions_type['j']
			elif instruction_name == 'beq':
				return instructions_type['beq']
			elif instruction_name == 'blt':
				return instructions_type['blt']
			elif instruction_name == 'bgt':
				return instructions_type['bgt']
			elif instruction_name == 'nop':
				return instructions_type['nop']
			elif instruction_name == 'div':
				return instructions_type['div']
			elif instruction_name == 'mflo':
				return instructions_type['mflo']
			elif instruction_name == 'mfhi':
				return instructions_type['mfhi']
			elif instruction_name == 'lw':
				return instructions_type['lw']
			elif instruction_name == 'sw':
				return instructions_type['sw']
			elif instruction_name == 'la':
				return instructions_type['la']
			elif instruction_name == 'slt':
				return instructions_type['slt']
			elif instruction_name == 'bne':
				return instructions_type['bne']
			elif instruction_name == 'lui':
				return instructions_type['lui']
			elif instruction_name == 'ori':
				return instructions_type['ori']
			else:
				return None

def get_instruction_opcode(mnemonic):
	if mnemonic:
		return instructions_opcode[mnemonic]

def R_Instruction(mnemonic,rs,rt,rd):
	#opcode = instruction_opcode[mnemonic]
	opcode = get_instruction_opcode(mnemonic)
	rs = get_register_code(rs)
	rt = get_register_code(rt)
	rd = get_register_code(rd)
	word = '{}{}{}{}{}{}'.format(opcode,rs,rt,rd,'00000',funct[mnemonic])
	return word

def J_Instruction(mnemonic,address):
	opcode = get_instruction_opcode(mnemonic)
	address = str(to_binary(address,26))
	word = '{}{}'.format(opcode,address)
	return word

def I_Instruction(mnemonic,rs,rt,imm):
	opcode = get_instruction_opcode(mnemonic)
	rt = get_register_code(rt)
	rs = get_register_code(rs)
	imm = int(imm)
	imm = to_binary(imm,16)
	word = '{}{}{}{}'.format(opcode,rs,rt,imm)
	return word

def encodeInstruction(lista):	
	if lista:
		tipo = get_instruction_type(lista[0])
		if tipo == 'R':
			if lista[0] == 'mfhi' or lista[0] == 'mflo':
				return R_Instruction(lista[0],'000000','000000',lista[1])
			else:
				return R_Instruction(lista[0],lista[2],lista[3],lista[1])
		elif tipo == 'I':
			if lista[0] == 'lw' or lista[0] == 'sw':
				return I_Instruction(lista[0],lista[3],lista[1],lista[2])
			elif lista[0] == 'la':
				return I_Instruction(lista[0],'$zero',lista[1],lista[2])
			elif lista[0] == 'beq' or lista[0] == 'blt' or lista[0] == 'bgt':
				return I_Instruction(lista[0],lista[2],lista[1],lista[3])
			else:
				return I_Instruction(lista[0],lista[2],lista[1],lista[3])
		elif tipo == 'J':
			return J_Instruction(lista[0],lista[1])
		else:
			return None

def updateControlUnit():
	word = IF_ID['Instruction']
	#### MAIN Control #####
	opcode = getOpcode(word)
	if  opcode == '000000': # Instruccion tipo R
		CONTROL_UNIT['ALUOp1'] = 1
		CONTROL_UNIT['ALUOp2'] = 0
		CONTROL_UNIT['RegDst'] = 1
		CONTROL_UNIT['MemRead'] = 0
		CONTROL_UNIT['MemWrite'] = 0
		CONTROL_UNIT['MemtoReg'] = 0
		CONTROL_UNIT['ALUSrc'] = 0
		CONTROL_UNIT['RegWrite'] = 1
		CONTROL_UNIT['Branch'] = 0
	elif opcode == instructions_opcode['lw']: #Instruccion LW
		CONTROL_UNIT['ALUOp1'] = 0
		CONTROL_UNIT['ALUOp2'] = 0
		CONTROL_UNIT['RegDst'] = 0
		CONTROL_UNIT['MemRead'] = 1
		CONTROL_UNIT['MemWrite'] = 0
		CONTROL_UNIT['MemtoReg'] = 1
		CONTROL_UNIT['ALUSrc'] = 1
		CONTROL_UNIT['RegWrite'] = 1
		CONTROL_UNIT['Branch'] = 0
	elif opcode == instructions_opcode['sw']: #Instruction SW
		CONTROL_UNIT['ALUOp1'] = 0
		CONTROL_UNIT['ALUOp2'] = 0
		CONTROL_UNIT['RegDst'] = 0
		CONTROL_UNIT['MemRead'] = 0
		CONTROL_UNIT['MemWrite'] = 1
		CONTROL_UNIT['MemtoReg'] = 0
		CONTROL_UNIT['ALUSrc'] = 1
		CONTROL_UNIT['RegWrite'] = 0
		CONTROL_UNIT['Branch'] = 0
	elif opcode == instructions_opcode['j']: #Instruction tipo J
		CONTROL_UNIT['ALUOp1'] = 1
		CONTROL_UNIT['ALUOp2'] = 1
		CONTROL_UNIT['RegDst'] = 0
		CONTROL_UNIT['MemRead'] = 0
		CONTROL_UNIT['MemWrite'] = 0
		CONTROL_UNIT['MemtoReg'] = 0
		CONTROL_UNIT['ALUSrc'] =  0
		CONTROL_UNIT['RegWrite'] = 0
		CONTROL_UNIT['Branch'] = 1
	elif opcode == instructions_opcode['beq'] or opcode == instructions_opcode['bgt'] or opcode == instructions_opcode['blt']: #Instruction tipo I beq,bgt,blt
		CONTROL_UNIT['ALUOp1'] = 0
		CONTROL_UNIT['ALUOp2'] = 1
		CONTROL_UNIT['RegDst'] = 0
		CONTROL_UNIT['MemRead'] = 0
		CONTROL_UNIT['MemWrite'] = 0
		CONTROL_UNIT['MemtoReg'] = 0
		CONTROL_UNIT['ALUSrc'] = 0
		CONTROL_UNIT['RegWrite'] = 0
		CONTROL_UNIT['Branch'] = 1
	elif opcode == instructions_opcode['la']: #Instruction tipo I la
		CONTROL_UNIT['ALUOp1'] = 1
		CONTROL_UNIT['ALUOp2'] = 1
		CONTROL_UNIT['RegDst'] = 0
		CONTROL_UNIT['MemRead'] = 0
		CONTROL_UNIT['MemWrite'] = 0
		CONTROL_UNIT['MemtoReg'] = 0
		CONTROL_UNIT['ALUSrc'] = 1
		CONTROL_UNIT['RegWrite'] = 1
		CONTROL_UNIT['Branch'] = 0
	elif opcode == instructions_opcode['addi']: #Instruction tipo I addi
		CONTROL_UNIT['ALUOp1'] = 1
		CONTROL_UNIT['ALUOp2'] = 1
		CONTROL_UNIT['RegDst'] = 0
		CONTROL_UNIT['MemRead'] = 0
		CONTROL_UNIT['MemWrite'] = 0
		CONTROL_UNIT['MemtoReg'] = 0
		CONTROL_UNIT['ALUSrc'] = 1
		CONTROL_UNIT['RegWrite'] = 1
		CONTROL_UNIT['Branch'] = 0
	elif opcode == instructions_opcode['div']: #Instruction tipo R div
		CONTROL_UNIT['ALUOp1'] = 1
		CONTROL_UNIT['ALUOp2'] = 1
		CONTROL_UNIT['RegDst'] = 1
		CONTROL_UNIT['MemRead'] = 0
		CONTROL_UNIT['MemWrite'] = 0
		CONTROL_UNIT['MemtoReg'] = 0
		CONTROL_UNIT['ALUSrc'] = 0
		CONTROL_UNIT['RegWrite'] = 1
		CONTROL_UNIT['Branch'] = 0
	elif opcode == instructions_opcode['mul']: #Instruction tipo R mul
		CONTROL_UNIT['ALUOp1'] = 1
		CONTROL_UNIT['ALUOp2'] = 1
		CONTROL_UNIT['RegDst'] = 1
		CONTROL_UNIT['MemRead'] = 0
		CONTROL_UNIT['MemWrite'] = 0
		CONTROL_UNIT['MemtoReg'] = 0
		CONTROL_UNIT['ALUSrc'] = 0
		CONTROL_UNIT['RegWrite'] = 1
		CONTROL_UNIT['Branch'] = 0
	elif opcode == instructions_opcode['mflo'] or opcode == instructions_opcode['mfhi']: #Instruction tipo R mul
		CONTROL_UNIT['ALUOp1'] = 1
		CONTROL_UNIT['ALUOp2'] = 1
		CONTROL_UNIT['RegDst'] = 1
		CONTROL_UNIT['MemRead'] = 0
		CONTROL_UNIT['MemWrite'] = 0
		CONTROL_UNIT['MemtoReg'] = 0
		CONTROL_UNIT['ALUSrc'] = 0
		CONTROL_UNIT['RegWrite'] = 1
		CONTROL_UNIT['Branch'] = 0

def updateALUControlUnit():
	funct = ID_EX['Funct']
	ALUOp1 = ID_EX['ALUOp1']
	ALUOp2 = ID_EX['ALUOp2']
	ALU_CONTROL_UNIT['ALUControlOut'] = alu_operations[funct]

def ALU_operate():
	ALU['Control'] = ALU_CONTROL_UNIT['ALUControlOut']
	ALU['Result'] = 0
	ALU['Zero'] = 0
	if ALU['Control'] == '0000': #add
		ALU['Result'] = ALU['A'] + ALU['B']
	elif ALU['Control'] == '0001': #mul
		ALU['Result'] = ALU['A'] * ALU['B']
	elif ALU['Control'] == '0010': #nop
		ALU['Result'] = 0
	elif ALU['Control'] == '0011': #div
		R[registers['lo']] = ALU['A']/ALU['B']
		R[registers['hi']] = ALU['A']%ALU['B']
	elif ALU['Control'] == '0100': #mflo
		ALU['Result'] = ALU['A']
	elif ALU['Control'] == '0101': #mfhi
		ALU['Result'] = ALU['A']
	elif ALU['Control'] == '0110': #addi
		ALU['Result'] = ALU['A'] + ALU['B']
	elif ALU['Control'] == '0111': #lw
		ALU['Result'] = ALU['A'] + ALU['B']
	elif ALU['Control'] == '1000': #sw
		ALU['Result'] = ALU['A'] + ALU['B']
	elif ALU['Control'] == '1001': #beq
		if ALU['A'] == ALU['B']:
			ALU['Zero']  = 1			
	elif ALU['Control'] == '1010': #blt
		if ALU['A'] <  ALU['B']:
			ALU['Zero']  = 1
	elif ALU['Control'] == '1011': #bgt
		if ALU['A'] > ALU['B']:
			ALU['Zero']  = 1
	elif ALU['Control'] == '1100': #la
		ALU['Result'] = ALU['B']
	elif ALU['Control'] == '1101': #j
		ALU['Zero'] = 1



#Funcion que obtiene todas las instrucciones desde un archivo dejandolas en una matriz
#@param1 ruta Nombre de la ruta del archivo
#return matriz con instrucciones
def leerArchivo(ruta):
	file=open(ruta,'r')
	i=0
	global LIMITE
	LIMITE =0
	labels = {}
	#PASADA 1 para identificar las LABEL y su posicion
	for linea in file:
		linea = linea.replace(',',' ').split()
		if linea:
			if len(linea) != 0:
				if len(linea) == 1: #LABEL
					labels[linea[0].replace(':','')] = i+1
				i+=1
				LIMITE+=1
	file.close()
	LIMITE +=1		
	file=open(ruta,'r')
	#PASADA 2 para agregar lineas y cambiar las label a medida que salen
	for linea in file:
		linea = linea.replace(',',' ').split()
		if linea:
			if len(linea) != 0:
				if len(linea) == 2: # JUMP o mfhi o mflo
					nueva = []
					if linea[0] == 'j':
						nueva.append(linea[0])
						nueva.append(labels[linea[1]])
					elif linea[0] == 'mfhi' or linea[0] == 'mflo':
						nueva.append(linea[0])
						nueva.append(linea[1])
					instructions_memory.append(nueva)
				elif len(linea) == 3: # I-Type lw la sw
					nueva = []
					if linea[0] == 'lw' or linea[0] == 'sw' or linea[0] == 'la':
						imm_rs = linea[2]
						descomp = imm_rs.replace('(',' ').replace(')',' ').split()
						if len(descomp) == 1: #la
							nueva.append(linea[0])
							nueva.append(linea[1])
							if descomp[0] != 'ARREGLO':
								nueva.append(labels[descomp[0]])
							else:
								nueva.append(0)
						else:
							nueva.append(linea[0])
							nueva.append(linea[1])
							nueva.append(descomp[0])
							nueva.append(descomp[1])
					
					instructions_memory.append(nueva)				
				elif len(linea) == 4: # R-Type or I-Type
					nueva = []
					if linea[0] == 'beq' or linea[0] == 'blt' or linea[0] == 'bgt':
						nueva.append(linea[0])
						nueva.append(linea[1])
						nueva.append(linea[2])
						nueva.append(labels[linea[3]])
					else:
						nueva =linea
					instructions_memory.append(nueva)
				i+=1
	file.close()
	return 0

def dump_registers():
	file = open('END_STATE.txt','w');
	actual_time = str(datetime.datetime.now())
	file.write('Last update: '+ actual_time + '\n')
	for register, valor in registers.items():
		if register == '$zero':
			file.write('$zero: '+ str(R[valor])+'\n')
		elif register == '$v0':
			file.write('$v0: '+ str(R[valor])+'\n')
		elif register == '$v1':
			file.write('$v1: '+ str(R[valor])+'\n')
		elif register == '$a0':
			file.write('$a0: '+ str(R[valor])+'\n')
		elif register == '$a1':
			file.write('$a1: '+ str(R[valor])+'\n')
		elif register == '$a2':
			file.write('$a2: '+ str(R[valor])+'\n')
		elif register == '$a3':
			file.write('$a3: '+ str(R[valor])+'\n')
		elif register == '$t0':
			file.write('$t0: '+ str(R[valor])+'\n')
		elif register == '$t1':
			file.write('$t1: '+ str(R[valor])+'\n')
		elif register == '$t2':
			file.write('$t2: '+ str(R[valor])+'\n')
		elif register == '$t3':
			file.write('$t3: '+ str(R[valor])+'\n')
		elif register == '$t4':
			file.write('$t4: '+ str(R[valor])+'\n')
		elif register == '$t5':
			file.write('$t5: '+ str(R[valor])+'\n')
		elif register == '$t6':
			file.write('$t6: '+ str(R[valor])+'\n')
		elif register == '$t7':
			file.write('$t7: '+ str(R[valor])+'\n')
		elif register == '$t8':
			file.write('$t8: '+ str(R[valor])+'\n')
		elif register == '$t9':
			file.write('$t9: '+ str(R[valor])+'\n')
		elif register == 'hi':
			file.write('hi: '+ str(R[valor])+'\n')
		elif register == 'lo':
			file.write('lo: '+ str(R[valor])+'\n')
	file.close()
	return 0

def updateRegistros():
	### READING REGISTERS ###
	word = IF_ID['Instruction']
	rs= getRs(word)
	rt =getRt(word)
	rd =getRd(word)
	REGISTROS['ReadReg1'] = rs
	REGISTROS['ReadReg2'] = rt
	### WRITING DATA ###
	REGISTROS['ReadData1'] = R[rs]
	REGISTROS['ReadData2'] = R[rt]

def updateBufferIF_ID(PC_4,IR):
	IF_ID['PC+4'] = PC_4
	IF_ID['Instruction'] = IR

def updateBufferID_EX():
	word = IF_ID['Instruction']
	ID_EX['PC+4'] = IF_ID['PC+4']
	ID_EX['Branch'] = CONTROL_UNIT['Branch']
	ID_EX['MemRead'] = CONTROL_UNIT['MemRead']
	ID_EX['MemtoReg'] = CONTROL_UNIT['MemtoReg']
	ID_EX['MemWrite'] = CONTROL_UNIT['MemWrite']
	ID_EX['ALUOp1'] = CONTROL_UNIT['ALUOp1']
	ID_EX['ALUOp2'] = CONTROL_UNIT['ALUOp2']
	ID_EX['ALUSrc'] = CONTROL_UNIT['ALUSrc']
	ID_EX['RegWrite'] = CONTROL_UNIT['RegWrite']
	ID_EX['ReadData1'] = REGISTROS['ReadData1']
	ID_EX['ReadData2'] = REGISTROS['ReadData2']
	ID_EX['Sign-extend_imm'] = sign_extend(getImm(word))
	ID_EX['Rt'] = getRt(word)
	ID_EX['Rd'] = getRd(word)
	ID_EX['RegDst'] = CONTROL_UNIT['RegDst']
	ID_EX['Opcode'] = getOpcode(word)
	if ID_EX['Opcode'] == '000000':
		ID_EX['Funct'] = getFunct(word)
	elif ID_EX['Opcode'] == instructions_opcode['j']:
		ID_EX['Funct'] = funct['j']
	elif ID_EX['Opcode'] == instructions_opcode['beq']:
		ID_EX['Funct'] = funct['beq']
	elif ID_EX['Opcode'] == instructions_opcode['addi']:
		ID_EX['Funct'] = funct['addi']
	elif ID_EX['Opcode'] == instructions_opcode['lw']:
		ID_EX['Funct'] = funct['lw']
	elif ID_EX['Opcode'] == instructions_opcode['sw']:
		ID_EX['Funct'] = funct['sw']
	elif ID_EX['Opcode'] == instructions_opcode['blt']:
		ID_EX['Funct'] = funct['blt']
	elif ID_EX['Opcode'] == instructions_opcode['bgt']:
		ID_EX['Funct'] = funct['bgt']
	elif ID_EX['Opcode'] == instructions_opcode['la']:
		ID_EX['Funct'] = funct['la']




def updateBufferEX_MEM():
	EX_MEM['Add_result'] = add_sl2()
	EX_MEM['Branch'] = ID_EX['Branch']
	EX_MEM['MemRead'] = ID_EX['MemRead']
	EX_MEM['MemtoReg'] = ID_EX['MemtoReg']
	EX_MEM['MemWrite'] = ID_EX['MemWrite']
	EX_MEM['RegWrite'] = ID_EX['RegWrite']
	EX_MEM['ReadData2'] = ID_EX['ReadData2']
	EX_MEM['Zero'] = ALU['Zero']
	EX_MEM['ALU_Output'] = ALU['Result']
	return 0

def updateBufferMEM_WB():
	MEM_WB['MemtoReg'] = EX_MEM['MemtoReg']
	MEM_WB['RegWrite'] = EX_MEM['RegWrite']
	MEM_WB['ALU_Output'] = EX_MEM['ALU_Output']
	MEM_WB['MUXRegDst_Output'] = EX_MEM['MUXRegDst_Output']

def add_sl2():
	#return (to_decimal(ID_EX['Sign-extend_imm'])<<2) + ID_EX['PC+4']
	return to_decimal(ID_EX['Sign-extend_imm'])+1

def sign_extend(imm):
	largo = len(imm)
	nueva = ''
	if largo == 16  and imm[0] == '0':
		ceros = '0' * (32 -largo)
		nueva = ceros+imm
	return nueva

def checkBranch():
	if EX_MEM['Branch'] == 1 and EX_MEM['Zero'] == 1:
		muxes['PCSrc'] = 1
		print "!!!!!!!!!!!!!WARNING!!!!!!!!!!!!!!!!!!!!!BRANCH!!!!!!!!!!!!!!WARNING!!!!!!!!!!!!!!!!"
	else:
		muxes['PCSrc'] = 0

def getOpcode(word):
	return word[0:6]

def getRs(word):
	return word[6:11]

def getRt(word):
	return word[11:16]

def getRd(word):
	return word[16:21]

def getShamt(word):
	return word[21:26]

def getFunct(word):
	return word[26:32]

def getImm(word):
	return word[16:32]

def to_decimal(num):
	i = len(num)-1
	total = 0
	exp = 0
	while i>=0:
		if num[i] == '1':
			total = total + pow(2,exp)
		exp += 1
		i-=1
	return total

def to_binary(decimal, length):
    '''
    Given a decimal, generate the binary equivalent string of
    given length.
    e.g. binary(2, 5) = 00010
    '''
    b = bitstring.Bits(int=decimal, length=length)
    return b.bin

def IF():
	print '#################### INSTRUCTION FETCH ####################'
	global PC
	print 'PC: '+str(PC) + ' -> ' + str(instructions_memory[PC])
	IR = encodeInstruction(instructions_memory[PC]) #Acceder a instruccion memory en el index de PC y codificarla a 32 bits
	print 'IR: '+ str(IR)
	PC_4 =PC+1
	print 'MUX PCSrc: ' + str(muxes['PCSrc'])
	if muxes['PCSrc'] == 1:
		PC = EX_MEM['Add_result']
	elif muxes['PCSrc'] == 0:
		PC = PC_4
	updateBufferIF_ID(PC_4,IR)
	print 'IF/ID-> '+ str(IF_ID)
	return 0

def ID():
	print '#################### INSTRUCTION DECODE ####################'
	updateControlUnit()
	print 'CONTROL UNIT-> '+ str(CONTROL_UNIT)
	updateRegistros()
	print 'REGISTER MEMORY-> '+ str(REGISTROS)
	updateBufferID_EX()
	return 0

def EX():
	print '#################### EXECUTION ####################'
	print 'ID/EX-> '+ str(ID_EX)
	updateALUControlUnit()
	print 'ALU CONTROL UNIT-> '+ str(ALU_CONTROL_UNIT)
	ALU['A'] = ID_EX['ReadData1']
	if ID_EX['ALUSrc'] == 0:
		ALU['B'] = ID_EX['ReadData2']
	elif ID_EX['ALUSrc'] == 1:
		ALU['B'] = to_decimal(ID_EX['Sign-extend_imm'])
	ALU_operate()
	if ID_EX['RegDst'] == 0:
		EX_MEM['MUXRegDst_Output'] = ID_EX['Rt']
	elif ID_EX['RegDst'] == 1:
		EX_MEM['MUXRegDst_Output'] = ID_EX['Rd']
	print 'ALU-> '+str(ALU)	
	updateBufferEX_MEM()
	return 0

def MEM():
	print '#################### MEM ####################'
	print 'EX/MEM-> '+ str(EX_MEM)
	checkBranch()
	ALUout = EX_MEM['ALU_Output']
	if EX_MEM['MemRead'] == 1 and EX_MEM['MemWrite'] == 0:
		MDR = ARREGLO[ALUout]
		MEM_WB['ReadData'] = MDR
	elif EX_MEM['MemRead'] == 0 and EX_MEM['MemWrite'] == 1:
		ARREGLO[ALUout] = EX_MEM['ReadData2']
	updateBufferMEM_WB()
	return 0

def WB():
	print '#################### WRITE BACK ####################'
	print 'MEM/WB-> '+ str(MEM_WB)
	if MEM_WB['MemtoReg'] == 1:
		print 'Esto hay en el registro, previo escritura :'+str(R[resgistro_destino])
		REGISTROS['WriteReg'] = MEM_WB['MUXRegDst_Output']
		R[REGISTROS['WriteReg']] = MEM_WB['ReadData']
	elif MEM_WB['MemtoReg'] == 0:
		REGISTROS['WriteReg'] = MEM_WB['MUXRegDst_Output']
		R[REGISTROS['WriteReg']] = MEM_WB['ALU_Output']
	return 0



### BLOQUE PRINCIPAL ###

if len(sys.argv) == 2:
	leerArchivo(sys.argv[1])
	#for i in  instructions_memory:
	#	print i
	print 'PARTE EJECUCION'
	##CICLO 1
	IF()
	##CICLO 2
	ID()
	IF()
 	##CICLO 3
	EX()
	ID()
	IF()
	##CICLO 4
	MEM()
	EX()
	ID()
	IF()
	##CICLO 5
	WB()
	MEM()
	EX()
	ID()
	IF()
	##CICLO 6
	WB()
	MEM()
	EX()
	ID()
	##CICLO 7
	WB()
	MEM()
	EX()
	##CICLO 8
	WB()
	MEM()
	##CICLO 9
	WB()
	
	dump_registers()
else:
	print 'Faltan argumentos\n'