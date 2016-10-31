import sys
import datetime
import bitstring

### DEFINICION DE VARIABLES GLOBALES ####
IF_flag = 0
ID_flag = 0
EX_flag = 0
MEM_flag = 0
WB_flag = 0
PC = 0
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
	'slt':'R',
	'bne':'I',
	'lui':'I',
	'ori':'I'
	}
instructions_opcode= {
	'add':'000000',
	'addi':'001000',
	'mul':'000000',
	'j':'000010',
	'beq':'000100',
	'nop': '000000' ,
	'div': '000000',
	'mflo':'000000',
	'mfhi':'000000',
	'lw':'100011',
	'sw':'101011',
	'slt':'000000',
	'bne':'000101',
	'lui':'001111',
	'ori':'001101',
	'blt':'111100',
	'bgt':'111110',
	'la':'111000'
	}
registers = {
	'$zero': '00000',
	'$v0': '00001',
	'$v1': '00010',
	'$a': '00011',
	'$a1': '00100',
	'$a2': '00101',
	'$a3': '00110',
	'$t''': '00111',
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
state = {
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
funct = {
	'add':'010100',
	'addi':None,
	'mul':'000000',
	'j':None,
	'beq':None,
	'nop': '000000' ,
	'div': '011010',
	'mflo':'001100',
	'mfhi':'001010',
	'lw':None,
	'sw':None,
	'slt':'101010',
	'bne':None,
	'lui':None,
	'ori':None,
	'blt':None,
	'bgt':None,
	'la':None
	}
alu_operations = {
	'add': '+',
	'sub': '-'
	}
control_unit = {'RegDst':0,'Branch':0,'MemRead':0,'MemtoReg':0,'ALUOp':'xx','MemWrite':0,'ALUSrc':0,'RegWrite':0}
muxes = {'RegDst': 0, 'ALUSrc': 0, 'MemtoReg': 0,'PCSrc': 0}
alu_control_unit = {'ALUControlOut': '011'}
register_mem = {'ReadReg1': '', 'ReadReg2': '','WriteReg': '', 'WriteData': 0, 'ReadData1': 0, 'ReadData2': 0}
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
	'ALUOp':'',
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
	'ALU_Result':0,
	'MUXRegDst_Output':''
	}
A = 0
B = 0

### IMPORTACION DE FUNCIONES Y CLASES####

### IMPLENTACION O DEFINICION DE FUNCIONES Y ClASES###
def get_register_code(reg):
	if reg:
		if reg == '$zero':
			return '00000'
		elif reg == '$v0':
			return '00001'
		elif reg == '$v1':
			return '00010'
		elif reg == '$a0':
			return '00011'
		elif reg == '$a1':
			return '00100'
		elif reg == '$a2':
			return '00101'
		elif reg == '$a3':
			return '00110'
		elif reg == '$t0':
			return '00111'
		elif reg == '$t1':
			return '01000'
		elif reg == '$t2':
			return '01001'
		elif reg == '$t3':
			return '01010'
		elif reg == '$t4':
			return '01011'
		elif reg == '$t5':
			return '01100'
		elif reg == '$t6':
			return '01101'
		elif reg == '$t7':
			return '01110'
		elif reg == '$t8':
			return '01111'
		elif reg == '$t9':
			return '10000'
		elif reg == 'lo':
			return '10001'
		elif reg == 'hi':
			return '10010'

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
			return R_Instruction(lista[0],lista[2],lista[3],lista[1])
		elif tipo == 'I':
			return I_Instruction(lista[0],lista[2],lista[1],lista[3])
		elif tipo == 'J':
			return J_Instruction(lista[0],lista[1])
		else:
			return None

def updateControlUnit():
	word = IF_ID['Instruction']
	#### ALU Control and MAIN Control #####
	opcode = getOpcode(word)
	if  opcode == '000000': # Instruccion tipo R
		control_unit['ALUOp'] = '10'
		control_unit['RegDst'] = 1
		control_unit['MemRead'] = 0
		control_unit['MemWrite'] = 0
		control_unit['MemtoReg'] = 0
		control_unit['ALUSrc'] = 0
		control_unit['RegWrite'] = 1
		control_unit['Branch'] = 0
	elif opcode == '100011': #Instruccion LW
		control_unit['ALUOp'] = '00'
		control_unit['RegDst'] = 0
		control_unit['MemRead'] = 1
		control_unit['MemWrite'] = 0
		control_unit['MemtoReg'] = 1
		control_unit['ALUSrc'] = 1
		control_unit['RegWrite'] = 1
		control_unit['Branch'] = 0
	elif opcode == '101011': #Instruction SW
		control_unit['ALUOp'] = '00'
		control_unit['RegDst'] = 0
		control_unit['MemRead'] = 0
		control_unit['MemWrite'] = 1
		control_unit['MemtoReg'] = 0
		control_unit['ALUSrc'] = 1
		control_unit['RegWrite'] = 0
		control_unit['Branch'] = 0
	elif opcode == '000010': #Instruction tipo J
		control_unit['ALUOp'] = 'xx'
		control_unit['RegDst'] = 0
		control_unit['MemRead'] = 0
		control_unit['MemWrite'] = 0
		control_unit['MemtoReg'] = 0
		control_unit['ALUSrc'] =  0
		control_unit['RegWrite'] = 0
		control_unit['Branch'] = 1
	elif opcode == '000100': #Instruction tipo I beq
		control_unit['ALUOp'] = '01'
		control_unit['RegDst'] = 0
		control_unit['MemRead'] = 0
		control_unit['MemWrite'] = 0
		control_unit['MemtoReg'] = 0
		control_unit['ALUSrc'] = 0
		control_unit['RegWrite'] = 0
		control_unit['Branch'] = 1

def updateALUControlUnit(funct):
	ALUOp = control_unit['ALUOp']
	if ALUOp == '00':
		alu_control_unit['ALUControlOut'] = '010' #add
	elif ALUOp == 'x1':
		alu_control_unit['ALUControlOut'] = '110' #sub
	elif ALUOp == '1x':
		funct = funct[2:5]
		if funct == '0000':	
			alu_control_unit['ALUControlOut'] = '010' #add
		elif funct == '0010':	
			alu_control_unit['ALUControlOut'] = '110' #sub
		elif funct == '0100':	
			alu_control_unit['ALUControlOut'] = '000' #and
		elif funct == '0101':	
			alu_control_unit['ALUControlOut'] = '001' #or
		elif funct == '1010':	
			alu_control_unit['ALUControlOut'] = '111' #slt

def updateRegisterMem():
	### READING REGISTERS ###
	word = IF_ID['Instruction']
	rs= getRs(word)
	print rs
	rt =getRt(word)
	rd =getRd(word)
	register_mem['ReadReg1']= rs
	register_mem['ReadReg2']= rt
	if control_unit['RegDst'] == 0:
		register_mem['WriteReg'] = rt
	else:
		register_mem['WriteReg'] = rd
	### WRITING DATA ###
	#register_mem['ReadData1'] = registers[rs]



#Funcion que obtiene todas las instrucciones desde un archivo dejandolas en una matriz
#@param1 ruta Nombre de la ruta del archivo
#return matriz con instrucciones
def leerArchivo(ruta):
	file=open(ruta,'r')
	i=0
	labels = []
	for linea in file:
		linea = linea.replace(' ,',' ').split()
		if linea:
			if len(linea) != 0:
				if len(linea) == 1: #LABEL
					instructions_memory.append(linea)
					labels.append([i,linea[0]])
				elif len(linea) == 2: # JUMP
					instructions_memory.append(linea)
				else: # R o I
					instructions_memory.append(linea)
			i+=1

	#print labels
	file.close()
	return 0

def dump_registers():
	file = open('END_STATE.txt','w');
	actual_time = str(datetime.datetime.now())
	file.write('Last update: '+ actual_time + '\n')
	for register, valor in registers.items():
		if register == '$zero':
			file.write('$zero: '+ str(state[valor])+'\n')
		elif register == '$v0':
			file.write('$v0: '+ str(state[valor])+'\n')
		elif register == '$v1':
			file.write('$v1: '+ str(state[valor])+'\n')
		elif register == '$a0':
			file.write('$a0: '+ str(state[valor])+'\n')
		elif register == '$a1':
			file.write('$a1: '+ str(state[valor])+'\n')
		elif register == '$a2':
			file.write('$a2: '+ str(state[valor])+'\n')
		elif register == '$a3':
			file.write('$a3: '+ str(state[valor])+'\n')
		elif register == '$t0':
			file.write('$t0: '+ str(state[valor])+'\n')
		elif register == '$t1':
			file.write('$t1: '+ str(state[valor])+'\n')
		elif register == '$t2':
			file.write('$t2: '+ str(state[valor])+'\n')
		elif register == '$t3':
			file.write('$t3: '+ str(state[valor])+'\n')
		elif register == '$t4':
			file.write('$t4: '+ str(state[valor])+'\n')
		elif register == '$t5':
			file.write('$t5: '+ str(state[valor])+'\n')
		elif register == '$t6':
			file.write('$t6: '+ str(state[valor])+'\n')
		elif register == '$t7':
			file.write('$t7: '+ str(state[valor])+'\n')
		elif register == '$t8':
			file.write('$t8: '+ str(state[valor])+'\n')
		elif register == '$t9':
			file.write('$t9: '+ str(state[valor])+'\n')
		elif register == 'hi':
			file.write('hi: '+ str(state[valor])+'\n')
		elif register == 'lo':
			file.write('lo: '+ str(state[valor])+'\n')
	file.close()
	return 0

def alu(A,B):
	return 0



def instruction_fetch():
	global PC
	IR = encodeInstruction(instructions_memory[PC]) #Acceder a instruccion memory en el index de PC y codificarla a 32 bits
	print IR
	PC_4 =PC+1
	#Almacena en el buffer entre etapas la instruccion de desde IF y el PC+4
	IF_ID['PC+4'] = PC_4
	IF_ID['Instruction'] = IR
	PC =PC_4
	return IF_ID

def instruction_decode():
	updateControlUnit()
	updateRegisterMem()
	return 0

def execution(rs,rt,rd):
	return 0

def data_memory(rs,rt,rd):
	return 0

def write_bach(rs,rt,rd):
	return 0

def to_binary(decimal, length):
    '''
    Given a decimal, generate the binary equivalent string of
    given length.
    e.g. binary(2, 5) = 00010
    '''
    b = bitstring.Bits(int=decimal, length=length)
    return b.bin

def add_4(entradaA):
	return entradaA + 1


def mux(linea_control, entradaA, entradaB):
	if linea_control:
		if linea_control == 1:
			return entradaA
		else:
			return entradaB

def getOpcode(word):
	return word[0:5]

def getRs(word):
	return word[6:10]

def getRt(word):
	return word[11:15]

def getRd(word):
	return word[16:20]

def getFunct(word):
	return word[27:31]

def getImm(word):
	return word[16:31]

### BLOQUE PRINCIPAL ###

if len(sys.argv) == 2:
	leerArchivo(sys.argv[1])
	#for elem in instructions_memory:
	#	print elem
	while PC < len(instructions_memory):
		SALIDA_IF = instruction_fetch()
		SALIDA_ID = instruction_decode()
	#print to_binary(20,6)
	#newR = R_Instruction('add','$t0','$t1','$t2')
	#newJ = J_Instruction('j',3)
	#newI = I_Instruction('addi','$t1','$t2',16)
	#print newR,newJ,newI
	dump_registers()
else:
	print('Faltan argumentos\n')
