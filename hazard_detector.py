import sys

if len(sys.argv) >= 2:
	file=open(argv[1],"r")
	instrucciones = []
	for linea in file:
		#linea = linea.replace(" ,"," ").split()
		instrucciones.append(linea)
	for inst in instrucciones:
		print(inst)
	file.close()


