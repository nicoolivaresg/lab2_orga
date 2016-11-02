addi $t0, $zero, 4
addi $t9, $zero, 1


add $t9, $zero, $t0

mul $t5, $t0, $t0
addi $t6, $zero, 2
div $t5, $t6
mflo $t7
add $t9, $t9, $t7


mul $t5, $t0, $t0
mul $t5, $t5, $t0
addi $t6, $zero, 6
div $t5, $t6
mflo $t7
add $t9, $t9, $t7

mul $t5, $t0, $t0
mul $t5, $t5, $t0
mul $t5, $t5, $t0
addi $t6, $zero, 24
div $t5, $t6
mflo $t7
add $t9, $t9, $t7

mul $t5, $t0, $t0
mul $t5, $t5, $t0
mul $t5, $t5, $t0
mul $t5, $t5, $t0
addi $t6, $zero, 120
div $t5, $t6
mflo $t7
add $t9, $t9, $t7

mul $t5, $t0, $t0
mul $t5, $t5, $t0
mul $t5, $t5, $t0
mul $t5, $t5, $t0
mul $t5, $t5, $t0
addi $t6, $zero, 720
div $t5, $t6
mflo $t7
add $t9, $t9, $t7

mul $t5, $t0, $t0
mul $t5, $t5, $t0
mul $t5, $t5, $t0
mul $t5, $t5, $t0
mul $t5, $t5, $t0
mul $t5, $t5, $t0
addi $t6, $zero, 5040
div $t5, $t6
mflo $t7
add $t9, $t9, $t7
