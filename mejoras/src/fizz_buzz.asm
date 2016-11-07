


addi $t0, $zero, 1
addi $t1, $zero, 100
addi $t7, $zero, 0
addi $t8, $zero, 0
addi $t9, $zero, 0




WHILE:
beq $t0, $t1, FIN
addi $t5, $zero, 15
div $t4, $t0, $t5
mfhi $t6
addi $t5, $zero, 15
beq $t6, $zero, FIZZBUZZ
addi $t5, $zero, 3
div $t4, $t0, $t5
mfhi $t6
beq $t6, $zero, FIZZ
addi $t5, $zero, 5
div $t4, $t0, $t5
mfhi $t6
beq $t6, $zero, BUZZ
j WHILE_CONT
FIZZBUZZ:
addi $t9, $t9, 1
j WHILE_CONT
FIZZ:
addi $t8, $t8, 1
j WHILE_CONT
BUZZ:
addi $t7, $t7, 1
j WHILE_CONT
WHILE_CONT:
addi $t0, $t0, 1
j WHILE





FIN:
