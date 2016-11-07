addi $t0, $zero, 5
addi $t1, $zero, 1
addi $t2, $zero, 1


WHILE:
beq $t0, $t1, FIN
mul $t2, $t0, $t2
addi $t0, $t0, -1
j WHILE
FIN:
