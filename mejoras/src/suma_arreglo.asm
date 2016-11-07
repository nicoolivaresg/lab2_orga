la $t1, ARREGLO
addi $t0, $zero, 1000
addi $t9, $zero, 0

WHILE:
beq $t9, $t0, END_WHILE
sw $t9, 0($t9)
addi $t9, $t9, 1
addi $t1, $t1, 4
j WHILE
END_WHILE:
addi $t0, $zero, -1
sw $t0, 0($t1)

la $t1, ARREGLO
addi $t0, $zero, 0

SUM:
addi $t2, $zero, -1
beq $t1, $t2, FIN
lw $t9, 0($t1)
add $t0, $t0, $t9
addi $t1, $t1, 4
j SUM


FIN:
