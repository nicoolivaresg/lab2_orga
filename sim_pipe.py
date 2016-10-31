import sys
import datetime
import bitstring

class Simulador(object):
	### DEFINICION DE CONSTANTES ####
	PC = 0
	instructions_type = {
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
	instructions_opcode = {
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
		'blt':'11110',
		'bgt':'11111',
		'la':'11100'
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
	control_unit = {'RegDst':0,'Branch':0,'MemRead':0,'MemtoReg':0,'ALUOp':00,'MemWrite':0,'ALUSrc':0,'RegWrite':0}
	instructions_memory = []
	IR = []

	### IMPORTACION DE FUNCIONES Y CLASES####

	### IMPLENTACION O DEFINICION DE FUNCIONES Y ClASES###
	def __init__(self, ruta):
		self.instructions_memory = leerArchivo(ruta)

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
				return '01110'
			elif reg == '$t7':
				return '01111'
			elif reg == '$t8':
				return '10000'
			elif reg == '$t9':
				return '10001'
			elif reg == 'lo':
				return '10010'
			elif reg == 'hi':
				return '01101'

	def R_Instruction(mnemonic,rs,rt,rd):
		#opcode = instruction_opcode[mnemonic]
		opcode = '000000'
		rs = get_register_code(rs)
		rt = get_register_code(rt)
		rd = get_register_code(rd)
		word = '{}{}{}{}{}{}'.format(opcode,rs,rt,rd,'00000',funct[mnemonic])
		return word

	def J_Instruction(mnemonic,address):
		opcode =instructions_opcode[mnemonic]
		address = str(to_binary(address,26))
		word = '{}{}'.format(opcode,address)
		return word

	def I_Instruction(mnemonic,rs,rt,imm):
		opcode = instruction_opcode[mnemonic]
		rt = get_register_code(rt)
		rd = get_register_code(rd)
		word = '{}{}{}{}'.format(opcode,rs,rt,imm)
		return word

	#Funcion que obtiene todas las instrucciones desde un archivo dejandolas en una matriz
	#@param1 ruta Nombre de la ruta del archivo
	#return matriz con instrucciones
	def leerArchivo(ruta):
		file=open(ruta,'r')
		i=0
		j=0
		for linea in file:
			linea = linea.replace(' ,',' ').split()
			if linea:
				instructions_memory.append(linea)
				i=i+1
		posiciones_labels = {}
		for inst in instructions_memory:
			if len(inst) == 1:
				print 'Cambiar j {} por j {}'.format(inst[0],j)
				posiciones_labels[inst[0]] = j
			j+=1
		for inst in instructions_memory:
			if len(inst) == 2:
				for label, index in posiciones_labels.items():
					if label.split(':')[0] == inst[0]:
						print inst[1], label,j
						inst[1] = index

		file.close()
		return instructions_memory




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

	def instruction_fetch(PC):
		IR = instructions_memory[PC]
		decodificada = [instruction_opcode(instructions_memory[PC]),instr]
		PC = PC + 1
		return IR

	def instruccion_decode():
		return 0

	def execution(rs,rt,rd):
		return 0

	def data_memory(rs,rt,rd):
		return 0

	def write_bach(rs,rt,rd):
		return 0


	def to_binary(decimal, length):
	    b = bitstring.Bits(int=decimal, length=length)
	    return b.bin


### BLOQUE PRINCIPAL ###
if len(sys.argv) == 2:
	#leerArchivo(sys.argv[1])
	sim = Simulador(sys.argv[1])
	for elem in sim.instructions_memory:
		print elem
	#while PC < len(instructions_memory):
		#IR = instruction_fetch(PC)
		#print IR
	#print to_binary(20,6)
	#nueva = R_Instruction('add','$t0','$t1','$t2')
	#print nueva
	dump_registers()
else:
	print('Faltan argumentos\n')
